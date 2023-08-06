import logging
from typing import Awaitable, Optional

from asyncio import Future
from pika import channel

from tornado.ioloop import IOLoop
from tornado.gen import multi, sleep

from pika.exceptions import AMQPConnectionError, ConnectionWrongStateError
from pika.adapters.tornado_connection import TornadoConnection
from pika.channel import Channel

from .exchange import Exchange
from .subscription import Consumer

from .adapters import declare_queue, get_channel, rabbit_connect
from .types import RabbitMQWorkerClientInterface


class RabbitMQWorkerClient(RabbitMQWorkerClientInterface):
    reconnect_delay = 5

    def __init__(self, host: str, port: int, login: str, password: str):
        self._url = f'amqp://{login}:{password}@{host}:{port}/%2F'  # FIXME: url encode login and password

        self._connection : Optional[TornadoConnection] = None
        self._channel : Optional[Channel] = None
        self.queue_name : Optional[str] = None
        self._connecting : Optional[Future] = None

        self.exchanges : dict[tuple[str, str], Exchange] = {}

        self.logger = logging.getLogger('%s.%s:%s' % (__name__, host, port))

    @property
    def _closing(self) -> bool:
        for exch in self.exchanges.values():
            if exch.subscriptions:
                return False

        return True

    async def subscribe(self, exchange: str, routing_key_pattern: str, consumer: Consumer) -> None:
        exch = self.exchanges.setdefault(
            exchange,
            Exchange(self, exchange)
        )

        await exch.add_subscription(routing_key_pattern, consumer)

    async def unsubscribe(self, exchange: str, routing_key_pattern: str) -> None:
        exch_key = exchange

        exch = self.exchanges.get(exch_key)

        if exch is None:
            self.logger.warning('exchange not registered: exch=%s', exchange)
            return

        await exch.remove_subscription(routing_key_pattern)

        if not exch.subscriptions:
            self.exchanges.pop(exch_key, None)

            if not self.exchanges:
                self.logger.info('no more exchanges, closing the channel')

                self.logger.debug('deleting queue')

                # no need to delete the queue: it is exclusive
                # await Task(self._channel.queue_delete, self.queue_name)

                self._channel.close()

    async def ensure_connected(self) -> Awaitable[Channel]:
        if self._connection is not None:
            return self._channel

        if self._connecting is not None:
            return self._connecting

        self._connecting = Future()

        # TODO: it should check self._closing too in the while guard
        # but doing so, ensure would not return channel anymore, but Opt[chan]
        # and callers should handle the None case
        # it happens if a subscription is canceled BEFORE being estabished
        while self._channel is None:
            self.logger.debug('connecting')

            try:
                self._connection = await rabbit_connect(self._url)

            except AMQPConnectionError as e:
                self.logger.error('connection failed: cause=%s, retray-delay=%s', e, self.reconnect_delay)

                await sleep(self.reconnect_delay)

                continue

            self.logger.info('connection opened')

            # This method adds an on close callback that will be invoked by pika
            # when RabbitMQ closes the connection to the publisher unexpectedly.
            self.logger.debug('adding connection close callback')

            self._connection.add_on_close_callback(self.on_connection_closed)

            self.logger.debug('creating new channel')

            self._channel = await get_channel(self._connection)

            self.logger.info('channel opened')

            self.queue_name = await declare_queue(self._channel, name='', exclusive=True)

            self.logger.debug('exclusive queue declared: name=%s', self.queue_name)

            # This method tells pika to call the on_channel_closed method if
            # RabbitMQ unexpectedly closes the channel.
            self.logger.debug('adding channel close callback')

            self._channel.add_on_close_callback(self.on_channel_closed)

            self._connecting.set_result(channel)
            self._connecting = None

        return self._channel

    def __str__(self):
        return '%s (%s)' % (self._url, 'connected' if self._connection is not None else 'disconnected')

    def on_connection_closed(self, connection, reason) -> None:
        """This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.

        :param pika.connection.Connection connection: The closed connection obj
        :param Exception reason: exception representing reason for loss of
            connection.

        """

        self._connection = None
        self._channel = None

        if self._closing:
            self.logger.info('connection closed and client is shutting down')

        else:
            self.logger.warning('connection closed: %s', reason)

            IOLoop.current().spawn_callback(self.reconnect)

    def on_channel_closed(self, channel, reason) -> None:
        """Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Channels are usually closed if you attempt to do something that
        violates the protocol, such as re-declare an exchange or queue with
        different parameters. In this case, we'll close the connection
        to shutdown the object.

        :param pika.channel.Channel channel: The closed channel
        :param Exception reason: why the channel was closed

        """
        self.logger.warning('channel %i was closed: %s', channel, reason)

        try:
            self._connection.close()

        except ConnectionWrongStateError:
            pass

    async def reconnect(self) -> None:
        """Will be invoked by the IOLoop timer if the connection is
        closed. See the on_connection_closed method.
        """

        await self.ensure_connected()

        await multi([
            exch.rebind_after_reconnection()
            for exch in self.exchanges.values()
        ])
