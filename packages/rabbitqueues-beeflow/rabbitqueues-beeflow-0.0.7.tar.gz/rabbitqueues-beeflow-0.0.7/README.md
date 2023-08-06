# Rabbit queues

Application to manage RabbitMQ queues

## Configuration

Into the `setup.py` file add:

```python
INSTALLED_APPS = [
    ...
    "rabbitqueues",
]
```

and add (i.e.):

```python
RABBITMQ_HOSTNAME = "localhost"
RABBITMQ_PORT = 5672
RABBITMQ_USERNAME = "rabbitusername"
RABBITMQ_PASSWORD = "supersecretpassword"
RABBITMQ_VHOST = "/"
```

### Own consumers

To prepare own conumer you need to create `class` which will extend `AbstractManager`. and register it in
dictionary `RABBITMQ_QUEUE_CONSUMERS = {"consumer_name": consumer_class}` in `setup.py`.

## Publish to the queue example

```python
import json
from django.conf import settings
from rabbitqueues import RabbitQueue


queue = RabbitQueue(settings.RABBITMQ_EMAIL_QUEUE)
queue.basic_publish(
    routing_key=settings.RABBITMQ_EMAIL_QUEUE,
    body=json.dumps(
        {
            "subject": "some subject",
            "email_from": settings.DEFAULT_FROM_EMAIL,
            "recipient_list": ["test@test.com"],
            "message": "This is the message for user.",
        }
    ),
)
queue.close()
```


