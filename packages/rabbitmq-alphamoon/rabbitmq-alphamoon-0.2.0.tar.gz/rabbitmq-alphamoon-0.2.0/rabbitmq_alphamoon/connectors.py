from __future__ import annotations

import abc
import json
import time
from contextlib import contextmanager
from threading import Thread
from typing import Any, Callable, Iterator, NamedTuple, Optional

import pika
from pika.connection import Parameters

from rabbitmq_alphamoon.logger import get_logger

LOGGER = get_logger('rabbitmq_alphamoon')


class IQueueConnector(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def consume_forever(self, process_message_callback: Callable[[Any], None]):
        pass

    @abc.abstractmethod
    def publish(self, message: Any) -> None:
        pass

    @property
    @abc.abstractmethod
    def message_count(self) -> int:
        pass


_RabbitMQConnection = NamedTuple(
    '_RabbitMQConnection',
    [
        ('connection', pika.BlockingConnection),
        ('channel', pika.adapters.blocking_connection.BlockingChannel),
        ('queue_declaration', pika.frame.Method),
    ],
)


class RabbitMQConnector(IQueueConnector):
    def __init__(
        self,
        connection_parameters: Parameters,
        queue: str,
        durable: bool = True,
        exclusive: bool = False,
        auto_delete: bool = False,
    ):
        self._connection_parameters = connection_parameters
        self._queue = queue
        self._durable = durable
        self._exclusive = exclusive
        self._auto_delete = auto_delete

        self._connection: Optional[_RabbitMQConnection] = None
        self._queue_declaration = None

    def _connect(self):
        LOGGER.debug("Connecting to broker, queue %s", self._queue)
        connection = pika.BlockingConnection(self._connection_parameters)
        channel = connection.channel()
        channel.confirm_delivery()
        queue_declaration = channel.queue_declare(
            queue=self._queue,
            durable=self._durable,
            exclusive=self._exclusive,
            auto_delete=self._auto_delete,
        )
        self._connection = _RabbitMQConnection(
            connection=connection,
            channel=channel,
            queue_declaration=queue_declaration,
        )
        LOGGER.info("Connection with broker established, queue %s", self._queue)

    def _assure_connection(self):
        while True:
            try:
                self._connect()
            except pika.exceptions.AMQPConnectionError as error:
                error_type = type(error).__name__  # e.g. 'AMQPConnectionError'
                LOGGER.warning("%s, queue %s: %s, retrying...", error_type, self._queue, error)
                time.sleep(1)
            else:
                break

    def _disconnect(self):
        LOGGER.debug("Disconnecting from broker, queue %s", self._queue)
        self._connection.connection.close()
        self._connection = None
        LOGGER.info("Disconnected from broker, queue %s", self._queue)

    @contextmanager
    def open_connection(self) -> Iterator[RabbitMQConnector]:
        self._assure_connection()
        try:
            yield self  # simplify one-time connector usage, especially when `consume_forever` used
        finally:
            self._disconnect()

    def _get_opened_connection(self) -> _RabbitMQConnection:
        if self._connection is None:
            raise RuntimeError("Connection not opened. Forgot to run in `open_connection` context?")
        return self._connection

    def _reconnect_and_get_opened_connection(self) -> _RabbitMQConnection:
        LOGGER.info("Reconnecting to queue, queue %s", self._queue)
        try:
            self._disconnect()
        except pika.exceptions.AMQPConnectionError as error:
            LOGGER.debug("Ignored disconnection error, queue %s, error %s", self._queue, error)
        else:
            LOGGER.warning("Connection was established, reconnecting anyway, queue %s", self._queue)

        self._assure_connection()
        return self._get_opened_connection()

    def consume_forever(self, process_message_callback: Callable[[Any], None]):
        connection = self._get_opened_connection()

        def callback_fun(
            channel: pika.channel.Channel,
            deliver: pika.spec.Basic.Deliver,
            properties: pika.BasicProperties,
            body: bytes,
        ):
            tag = deliver.delivery_tag
            LOGGER.info("Received message # %s, queue %s", tag, self._queue)

            def send_ack():
                channel.basic_ack(delivery_tag=tag)
                LOGGER.info("Sent ack for message # %s, queue %s", tag, self._queue)

            def process_fun():
                LOGGER.debug("Deserializing body of message # %s, queue %s", tag, self._queue)
                message = json.loads(body)

                LOGGER.info("Processing message # %s, queue %s", tag, self._queue)
                process_message_callback(message)

                try:
                    LOGGER.debug("Sending ack for message # %s, queue %s", tag, self._queue)
                    channel.connection.add_callback_threadsafe(send_ack)
                except pika.exceptions.AMQPError as error:
                    LOGGER.error(
                        "Sending ack failed for message # %s, queue %s, %s: %s",
                        tag,
                        self._queue,
                        type(error).__name__,  # type of an error, e.g. 'ConnectionClosedByBroker'
                        error,
                    )

            # Running the processing in separate thread allow for connection keep-alive as the main
            # thread is not being blocked by the processing.
            Thread(target=process_fun, name=f'message # {tag}, queue {self._queue}').start()

        try:
            while True:
                try:
                    LOGGER.debug("Starting consumption, queue %s", self._queue)
                    connection.channel.basic_qos(prefetch_count=1)  # this limits number of threads
                    connection.channel.basic_consume(
                        queue=self._queue,
                        on_message_callback=callback_fun,
                        auto_ack=False,
                    )
                    connection.channel.start_consuming()
                except KeyboardInterrupt:
                    break
                except pika.exceptions.AMQPConnectionError as error:
                    error_type = type(error).__name__  # e.g. 'ConnectionClosedByBroker'
                    LOGGER.warning("%s, queue %s: %s, retrying...", error_type, self._queue, error)
                    time.sleep(1)
                    connection = self._reconnect_and_get_opened_connection()
                except pika.exceptions.AMQPChannelError as error:
                    error_type = type(error).__name__  # e.g. 'ChannelWrongStateError'
                    LOGGER.error("%s, queue %s: %s, stopping...", error_type, self._queue, error)
                    break
        finally:
            LOGGER.debug("Stopping consumption, queue %s", self._queue)
            connection.channel.stop_consuming()

    def publish(self, message: Any) -> None:
        connection = self._get_opened_connection()
        LOGGER.debug("Serializing message, queue %s", self._queue)
        body = json.dumps(
            message,
            ensure_ascii=False,
            separators=(',', ':'),  # compact encoding
        )

        try:
            LOGGER.debug("Publishing message, queue %s", self._queue)
            connection.channel.basic_publish(
                exchange='',
                routing_key=self._queue,
                body=body.encode(),
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,  # persists during restarts
                ),
                mandatory=True,  # ack's when message is received
            )
            LOGGER.info("Published message, queue %s", self._queue)
        except pika.exceptions.UnroutableError as error:
            LOGGER.error("Publishing failed, queue %s, %s", self._queue, error)

    @property
    def message_count(self) -> int:
        connection = self._get_opened_connection()
        return connection.queue_declaration.method.message_count
