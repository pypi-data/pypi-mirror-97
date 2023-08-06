import logging
from typing import Awaitable, Optional

from asyncio import Future

from tornado.gen import multi

from pika.exchange_type import ExchangeType

from .subscription import Subscription, Consumer
from .types import RabbitMQWorkerClientInterface
from .adapters import declare_exchange


class Exchange:
    def __init__(self, client: RabbitMQWorkerClientInterface, exchange: str):
        self.client = client
        self.exchange = exchange
        self.exchange_type = ExchangeType.fanout
        self.declared : Optional[Future] = None

        self.subscriptions : dict[str, Subscription] = {}

        self.logger = logging.getLogger(client.logger.name + '.' + exchange)

    async def add_subscription(self, routing_key_pattern: str, consumer: Consumer) -> Awaitable[None]:
        s = self.subscriptions.setdefault(
            routing_key_pattern,
            Subscription(self, routing_key_pattern, consumer)
        )

        await self.declare()

        await s.setup()

    async def remove_subscription(self, routing_key_pattern: str) ->  Awaitable[None]:
        s = self.subscriptions.pop(routing_key_pattern, None)

        if s is None:
            self.logger.warning('unknown routing key pattern: routing_key_pattern=%s', routing_key_pattern)

            return

        if not self.subscriptions:
            self.logger.info('no more subscriptions, exchange will be removed')

    async def declare(self) -> Awaitable[None]:
        if self.declared is not None:
            await self.declared
            return

        self.declared = Future()

        channel = await self.client.ensure_connected()

        await declare_exchange(
            channel, self.exchange, self.exchange_type,
            passive=False,
            durable=False,
            auto_delete=True,
        )

        self.declared.set_result(True)

    async def rebind_after_reconnection(self) -> Awaitable[None]:
        self.declared = None

        await self.declare()

        await multi([
            s.rebind_after_reconnection()
            for s in self.subscriptions.values()
        ])

    def __str__(self):
        return '%s/%s:%s' % (self.client, self.exchange_type, self.exchange)
