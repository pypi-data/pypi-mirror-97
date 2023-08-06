from typing import Awaitable

from asyncio import Future

from pika import URLParameters, BaseConnection
from pika.adapters.tornado_connection import TornadoConnection
from pika.channel import Channel
from pika.frame import Method
from pika.spec import Channel, Queue
from pika.exchange_type import ExchangeType


def rabbit_connect(url: str):
    r = Future()

    def ok_cb(connection):
        # note: this is the same object TornadoConnection built below
        r.set_result(connection)

    def ko_cb(connection, failure):
        r.set_exception(failure)

    TornadoConnection(
        parameters=URLParameters(url),
        on_open_callback=ok_cb,
        on_open_error_callback=ko_cb,
    )

    return r


def get_channel(conn: BaseConnection) -> Awaitable[Channel]:
    r = Future()

    conn.channel(on_open_callback=lambda channel: r.set_result(channel))

    return r


def declare_exchange(channel: Channel, exchange: str, exchange_type: ExchangeType, passive: bool, durable: bool, auto_delete: bool) -> Awaitable[None]:
    r = Future()

    channel.exchange_declare(
        exchange,
        exchange_type,
        passive=passive,
        durable=durable,
        auto_delete=auto_delete,
        callback=lambda method_frame: r.set_result(None),
    )

    return r


def declare_queue(channel: Channel, name: str, exclusive: bool) -> Awaitable[str]:
    r = Future()

    def callback(method_frame: Method):
        method : Queue.DeclareOk = method_frame.method
        queue = method.queue

        r.set_result(queue)

    channel.queue_declare(name, exclusive=exclusive, callback=callback)

    return r


def bind_queue(channel: Channel, queue: str, exchange: str, routing_key_pattern: str) -> Awaitable[None]:
    r = Future()

    channel.queue_bind(queue, exchange, routing_key_pattern, callback=lambda method_frame: r.set_result(None))

    return r


def unbind_queue(channel: Channel, queue: str, exchange: str, routing_key_pattern: str) -> Awaitable[None]:
    r = Future()

    channel.queue_unbind(queue, exchange, routing_key_pattern, callback=lambda method_frame: r.set_result(None))

    return r


def basic_cancel(channel: Channel, consumer_tag: str) -> Awaitable[None]:
    r = Future()

    channel.basic_cancel(consumer_tag, callback=lambda method_frame: r.setFuture(None))

    return r
