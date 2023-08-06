# rabbitqm-alphamoon

![image](https://img.shields.io/pypi/v/rabbitmq-alphamoon.svg)
![image](https://img.shields.io/pypi/pyversions/rabbitmq-alphamoon.svg)

[pika](https://pypi.org/project/pika/)-based RabbitMQ connector with built in JSON serialization/deserialization

---

## Features
- publishing: `publish(message)`
- getting number of messages in the queue: `message_count`
- consuming (forever, i.e. with a callback function): `consume_forever(callback_fun)`

See code examples in the "Examples" section.

## Requirements

```requirements.txt
pika==1.2.0
```

## Installation

You can install "rabbitmq-alphamoon" via
[pip](https://pypi.org/project/pip/) from
[PyPI](https://pypi.org/project):

    $ pip install rabbitmq-alphamoon

## Examples

### Initialization
```python
import pika
from rabbitmq_alphamoon import RabbitMQConnector

parameters = pika.ConnectionParameters(
    host=rabbitmq_host,
    port=rabbitmq_port,
    credentials=pika.PlainCredentials(
        username=rabbitmq_username,
        password=rabbitmq_password,
    ),
)

queue = RabbitMQConnector(
    connection_parameters=parameters,
    queue=queue_name,
)
```

### Publishing
```python
message = {'foo': 'bar'}

with queue.open_connection():
    queue.publish(message)
```

### Getting a number of the messages in the queue
```python
message_count = queue.message_count
```

### Consuming
```python
def process_message(message):
    print(message)

with queue.open_connection():
    queue.consume_forever(process_message_callback=process_message)
```

### Short form for one-time usage of connector
If you do not need to reuse the connector, you can initialize and open connection without assignment of connector to a variable before calling `open_connection` context manager. This may come in handy especially in case of consuming, where connector is usually used only to call `consume_forever` function.
```python
with RabbitMQConnector(
    connection_parameters=parameters,
    queue=queue_name,
).open_connection() as queue:
   queue.consume_forever(process_message_callback=process_message)
```

## Contributing

Contributions are very welcome. Tests can be run with
[tox](https://tox.readthedocs.io/en/latest/), please ensure the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the
[MIT](http://opensource.org/licenses/MIT) license, "rabbitmq-alphamoon" is free and open source software

## Issues

If you encounter any problems, please email us at <dev@alphamoon.ai>, along with a detailed description.
