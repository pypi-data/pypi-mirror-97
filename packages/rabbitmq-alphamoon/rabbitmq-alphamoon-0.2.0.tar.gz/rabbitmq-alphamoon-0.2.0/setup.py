#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from setuptools import setup

import rabbitmq_alphamoon


def read(subpath):
    return (Path(__file__).parent / subpath).read_text(encoding='utf-8')


setup(
    name='rabbitmq-alphamoon',
    version=rabbitmq_alphamoon.__version__,
    author='Piotr Dąbrowski',
    author_email='piotr.dabrowski@alphamoon.ai',
    maintainer='Piotr Dąbrowski',
    maintainer_email='dev@alphamoon.ai',
    license='MIT',
    url='https://gitlab.com/alphamoon/internal_tools/rabbitmq-alphamoon',
    description='pika-based RabbitMQ connector with built in JSON serialization/deserialization',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    py_modules=['rabbitmq_alphamoon'],
    python_requires='>=3.8',
    install_requires=[
        'pika==1.2.0',
    ],
    packages=['rabbitmq_alphamoon'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
)
