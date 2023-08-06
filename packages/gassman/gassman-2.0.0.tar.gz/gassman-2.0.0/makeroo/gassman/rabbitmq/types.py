from typing import Any, Awaitable, Callable, Optional

import logging

from pika.channel import Channel


RoutingKey = str
Message = bytes
Consumer = Callable[[RoutingKey, Message], None]


class RabbitMQWorkerClientInterface:
    logger : logging.Logger = None

    queue_name : Optional[str] = None

    async def ensure_connected(self) -> Awaitable[Channel]:
        raise Exception('not implemented')


class ExchangeInterface:
    client : RabbitMQWorkerClientInterface = None

    exchange : str = None
