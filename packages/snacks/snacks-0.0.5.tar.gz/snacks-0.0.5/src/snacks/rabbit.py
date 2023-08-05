import ast
import json
import logging
import threading
import uuid
from inspect import signature
from typing import Optional, TypeVar

from pika import BlockingConnection, BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic

from snacks import APP
from snacks.rabbit_config import RabbitConfig

__all__ = ('Rabbit',)
log = logging.getLogger(APP)
T = TypeVar('T')


class Rabbit:
    """A class to interface with RabbitMQ."""

    def __init__(self, rabbit_config: RabbitConfig) -> None:
        self.config = rabbit_config

    def publish(self, body: any, routing_key: str, **kwargs) -> None:
        """Publish message to a rabbit queue with the given routing key.

        :param body: The message to publish.
        :param kwargs: Keyword args to pass to pika publish.
        :param routing_key: The routing key.
        """
        log.debug('Publishing key={} msg={}', routing_key, body)
        mq_conn = BlockingConnection(self.config.params)
        channel: BlockingChannel = mq_conn.channel()
        channel.basic_publish(
            exchange=self.config.exchange,
            routing_key=routing_key,
            body=_get_body(body),
            **kwargs
        )

    def publish_and_receive(self,
                            body: any,
                            routing_key: str,
                            response_type: T,
                            time_limit: int = 10,
                            headers: Optional[dict[str, any]] = None) -> T:
        """Publish message to a rabbit queue with the given routing key.

        :param body: The message to publish.
        :param routing_key: The routing key.
        :param response_type: Type to map the response to, must be
            annotated with @dataclass_json.
        :param time_limit: Amount of time to wait for a response,
            defaults to 10 seconds.
        :param headers: To publish with.
        """
        log.debug('Publishing key={} msg={}', routing_key, body)
        mq_conn = BlockingConnection(self.config.params)
        channel: BlockingChannel = mq_conn.channel()
        response: Optional[bytes] = None
        corr_id = str(uuid.uuid4())

        def _on_response(_channel: BlockingChannel,
                         _method: Basic.Deliver,
                         props: BasicProperties,
                         resp_body: bytes) -> None:
            nonlocal response
            if props.correlation_id == corr_id:
                response = resp_body

        result = channel.queue_declare(queue='', exclusive=True)
        callback_queue = result.method.queue
        channel.basic_consume(
            queue=callback_queue,
            on_message_callback=_on_response,
            auto_ack=True
        )
        channel.basic_publish(
            exchange=self.config.exchange,
            routing_key=routing_key,
            properties=BasicProperties(
                reply_to=callback_queue,
                correlation_id=corr_id,
                headers=headers
            ),
            body=_get_body(body)
        )
        mq_conn.process_data_events(time_limit=time_limit)
        return response_type.from_json(response)

    def listener(self, queues: list[str]) -> callable:
        """Decorate a function to make it a rabbit consumer.

        The decorated function can have as parameters, the message body,
        the method, the properties, or no parameters.

        :param queues: The queues to consume from.
        :return: Function decorated to be a rabbit consumer.
        """
        mq_conn = BlockingConnection(self.config.params)
        channel = mq_conn.channel()

        def wrapper(fun: callable) -> None:
            original_name = fun.__name__
            for queue in queues:
                fun.__name__ = f'listener_{queue}'
                _listen(channel, self.config.exchange, queue, fun)
                log.debug('{} subscribed to {}', original_name, queue)
            thread = threading.Thread(target=_consume, args=(channel,))
            thread.daemon = True
            thread.start()

        return wrapper


def _listen(channel: BlockingChannel,
            exchange: str,
            queue: str,
            fun: callable) -> None:
    def callback(ch: BlockingChannel,
                 method: Basic.Deliver,
                 properties: BasicProperties,
                 body: bytes) -> None:
        log.debug('{} received {}', queue, body)
        sig = signature(fun)
        kwargs: dict[str, any] = {}
        for name, param in sig.parameters.items():
            if name == 'self':
                kwargs[name] = None
            if param.annotation == BlockingChannel:
                kwargs[name] = ch
            elif param.annotation == method:
                kwargs[name] = method
            elif param.annotation == BasicProperties:
                kwargs[name] = properties
            elif param.annotation == str:
                kwargs[name] = body.decode('utf-8')
            elif param.annotation in {list, tuple, set, dict}:
                kwargs[name] = ast.literal_eval(body.decode('UTF-8'))
            elif param.annotation == bytes:
                kwargs[name] = body
            elif param.annotation in {int, float}:
                kwargs[name] = param.annotation(body)
            else:
                try:
                    kwargs[name] = param.annotation.from_dict(json.loads(body))
                except AttributeError:
                    try:
                        kwargs[name] = json.loads(body)
                    except json.decoder.JSONDecodeError:
                        kwargs[name] = body
        # noinspection PyBroadException
        try:
            resp = fun(**kwargs)
            if properties.reply_to:
                channel.basic_publish(
                    exchange=exchange,
                    routing_key=properties.reply_to,
                    properties=BasicProperties(
                        correlation_id=properties.correlation_id
                    ),
                    body=_get_body(resp)
                )
                channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            log.exception(msg=f'{type(e).__name__}: {e}', exc_info=e)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=queue,
        auto_ack=True,
        on_message_callback=callback
    )


def _consume(channel: BlockingChannel) -> None:
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
        channel.close()


def _get_body(body: any) -> bytes:
    if 'to_json' in dir(body):
        return body.to_json().encode()
    elif isinstance(body, bytes):
        return body
    else:
        return str(body).encode()
