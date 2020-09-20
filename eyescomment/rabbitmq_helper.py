#!/usr/bin/env python
# export PATH=$PATH:/usr/local/sbin
import pika
import json
import logging

logger = logging.getLogger(__name__)


class RabbitMqHelper():
    """" Rabbitmq instance"""
    def __init__(self, host='localhost', exchange='log', exchange_type='fanout'):
        """" Rabbitmq contructor

        Args:
            host(str)
            exchange(str)
            exchange_type(str)

        """
        self.host = host
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))
        self._queue_name = None
        self._channel = None

    @property
    def channel(self):
        if not self._channel:
            self._channel = self.connection.channel()
        return self._channel

    def _declare(self):
        self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type)

    def _bind(self):
        self._declare()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self._queue_name = result.method.queue
        self.channel.queue_bind(exchange=self.exchange, queue=self._queue_name)

    def publish(self, msg, routing_key=''):
        """ Rabbitmq publish

        Args:
            msg(dict): publish message

        """
        self._declare()
        message = json.dumps(msg)
        self.channel.basic_publish(exchange=self.exchange, routing_key=routing_key, body=message)

    def consume(self, callback, ack=False):
        """ Rabbitmq consume

        Args:
            callback(function): define callback(ch, method, properties, body)
            ack(bool):

        """
        self._bind()
        logger.info('RabbitMq start consuming')
        self.channel.basic_consume(
            queue=self._queue_name, on_message_callback=callback, auto_ack=ack)
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
