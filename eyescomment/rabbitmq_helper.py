#!/usr/bin/env python
# export PATH=$PATH:/usr/local/sbin
import pika
import json
import logging


logger = logging.getLogger(__name__)


class RabbitMqBase():
    """ Rabbitmq Base instance"""
    def __init__(self, host='localhost'):
        """ Rabbitmq contructor

        Args:
            host(str)

        """
        self.host = host
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host))
        self._channel = None

    @property
    def channel(self):
        if not self._channel:
            self._channel = self.connection.channel()
        return self._channel

    def publish(self, msg, exchange='', routing_key=''):
        """ Rabbitmq publish

        Args:
            msg(dict): publish message,
            exchange(str): rabbitmq exchange,
            routing_key(str): rabbitmq routing_key

        """
        message = json.dumps(msg, ensure_ascii=False)
        self.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)

    def consume(self, callback, queue_name='', ack=True):
        """ Rabbitmq consume

        Args:
            callback(function): define callback(ch, method, properties, body)
            ack(bool)

        """
        logger.info('RabbitMq start consuming')
        self.channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=ack)
        self.channel.start_consuming()

    def close(self):
        self.connection.close()


class RabbitMqFanout(RabbitMqBase):
    """ Rabbitmq Fanout instance"""
    def __init__(self, host='localhost', exchange='log'):
        """ Rabbitmq Fanout contructor

        Args:
            host(str)
            exchange(str)
            exchange_type(str)

        """
        super().__init__(host=host)
        self.exchange = exchange
        self.exchange_type = 'fanout'
        self._queue_name = None

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
            routing_key(str): rabbitmq routing_key

        """
        self._declare()
        super().publish(msg, exchange=self.exchange, routing_key=routing_key)

    def consume(self, callback, ack=True):
        """ Rabbitmq consume

        Args:
            callback(function): define callback(ch, method, properties, body)
            ack(bool)

        """
        self._bind()
        if self._queue_name:
            super().consume(
                callback=callback, queue_name=self._queue_name, ack=ack)
        else:
            logger.error('In RabbitMq fanout queue name is None')


class RabbitMqTasks(RabbitMqBase):
    """ Rabbitmq Tasks queue instance"""
    def __init__(self, host='localhost', exchange='', queue_name='', durable=None):
        """ Rabbitmq Tasks queue contructor

        Args:
            host(str)
            exchange(str)
            queue_name(str)

        """
        super().__init__(host=host)
        self.exchange = exchange
        self.queue_name = queue_name
        self.durable = durable

    def publish(self, msg, routing_key=''):
        """ Rabbitmq publish

        Args:
            msg(dict): publish message
            routing_key(str): rabbitmq routing_key

        """
        self.channel.queue_declare(queue=self.queue_name, durable=self.durable)
        super().publish(msg, exchange=self.exchange, routing_key=routing_key)

    def consume(self, callback, ack=True):
        """ Rabbitmq consume

        Args:
            callback(function): define callback(ch, method, properties, body)
            ack(bool)

        """
        self.channel.queue_declare(queue=self.queue_name, durable=self.durable)
        super().consume(
            callback=callback, queue_name=self.queue_name, ack=ack)
