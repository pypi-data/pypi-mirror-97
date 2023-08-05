# Snacks

Snacks is a wrapper around [pika](https://pypi.org/project/pika/) to
provide a convenient interface to publish/subscribe to queues in
RabbitMQ.

## Example
```python
from pika import BlockingConnection, PlainCredentials
from pika.adapters.blocking_connection import BlockingChannel

from snacks.rabbit import Rabbit
from snacks.rabbit_config import RabbitConfig

# Initial setup of configuration and Rabbit class.
config = RabbitConfig(
    host='localhost',
    port=5672,
    exchange_name='',
    credentials=PlainCredentials('snacks', 'snacks')
)
rabbit = Rabbit(config)
# Setup queues to use.
queue = 'snacks'
key = 'snackey'
mq_conn = BlockingConnection(rabbit.config.params)
channel: BlockingChannel = mq_conn.channel()
channel.exchange_declare(
    exchange=rabbit.config.exchange_name,
    exchange_type='topic',
    durable=True
)
channel.queue_declare(queue=queue, durable=True)
channel.queue_bind(
    exchange=rabbit.config.exchange_name,
    queue=queue,
    routing_key=key
)


@rabbit.listener([queue])
def listen(event: str) -> None:
    print(f'Received message: {event}')


if __name__ == '__main__':
    rabbit.publish('To a python, rabbits and pikas are snacks.', key)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('Exiting...')
```
