import json

from django.core.management.base import BaseCommand

from rabbitqueues import RabbitQueue, get_consumers, get_rabbit_database_queue_name, get_unknown_elements_queue_name


class Command(BaseCommand):
    help = "Consume DB QUEUE and send to correct queue managers."

    #  dict with consumers, which extends AbstractManager
    __managers = get_consumers()

    def handle(self, *args, **options):
        queue = RabbitQueue(get_rabbit_database_queue_name())
        queue.basic_consume(self.callback)
        queue.start_consuming()

    def callback(self, **kwargs):
        body = json.loads(kwargs.pop("body"))

        try:
            self.__managers[body["queue_engine"]]().execute(body["data"])
        except KeyError:
            self.send_to_unknown_engine(body)
            return

    @staticmethod
    def send_to_unknown_engine(body):
        queue = RabbitQueue(get_unknown_elements_queue_name())
        queue.basic_publish(routing_key=get_unknown_elements_queue_name(), body=json.dumps(body))
        queue.close()
