__version__ = "0.0.7"

import pika
from django.conf import settings
from pika.exceptions import StreamLostError

default_app_config = "rabbitqueues.apps.RabbitQueuesConfig"


def get_rabbit_hostname():
    return getattr(settings, "RABBITMQ_HOSTNAME")


def get_rabbit_port():
    return int(getattr(settings, "RABBITMQ_PORT"))


def get_rabbit_vhostname():
    return getattr(settings, "RABBITMQ_VHOST")


def get_rabbit_username():
    return getattr(settings, "RABBITMQ_USERNAME")


def get_rabbit_password():
    return getattr(settings, "RABBITMQ_PASSWORD")


def get_rabbit_database_queue_name():
    return getattr(settings, "RABBITMQ_DATABASE_QUEUE", "database_queue")


def get_unknown_elements_queue_name():
    return getattr(settings, "RABBITMQ_UNKNOWN_ELEMENTS_QUEUE", "unknown_elements_queue")


def get_consumers() -> dict:
    return getattr(settings, "RABBITMQ_QUEUE_CONSUMERS", {})


class RabbitQueue:
    """RabbitMQ queue consumer and producer."""

    def __init__(self, queue: str):
        """Initialize channel and queue."""
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=get_rabbit_hostname(),
                port=get_rabbit_port(),
                virtual_host=get_rabbit_vhostname(),
                credentials=pika.credentials.PlainCredentials(
                    username=get_rabbit_username(), password=get_rabbit_password()
                ),
            )
        )
        self.channel = self.connection.channel()
        self.queue = queue
        self.channel.queue_declare(queue=queue)

    def basic_publish(self, routing_key, body):
        self.channel.basic_publish(exchange="", routing_key=routing_key, body=body)

    def basic_consume(self, on_message_callback, auto_ack: bool = True):
        self.channel.basic_consume(queue=self.queue, auto_ack=auto_ack, on_message_callback=on_message_callback)

    def start_consuming(self):
        try:
            self.channel.start_consuming()
        except StreamLostError:
            self.start_consuming()

    def close(self):
        self.connection.close()
