import logging
from typing import Any, Callable, Optional

from asyncio import Future

from pika.channel import Channel

from .types import Consumer, ExchangeInterface, Message
from .adapters import basic_cancel, bind_queue, unbind_queue


class Subscription (object):
    def __init__(self, exchange: ExchangeInterface, routing_key_pattern: str, consumer: Consumer):
        self.routing_key_pattern = routing_key_pattern
        self.exchange = exchange
        self.consumer = consumer

        self._consumer_tag : Optional[str] = None

        # a future resolved once the setup is complete
        # if None no initialization has been down OR the shutdown completed
        # thus pending_initialization is not None when the subscription is initializing or is running
        self.pending_initialization : Future = None
        # a future resolved once the shutdown is complete
        # if None no shutdown process is running
        self.pending_shutdown = None

        self.logger = logging.getLogger(exchange.logger.name + '.' + routing_key_pattern)

#    @coroutine
#    def add_consumer(self, consumer):
#        if consumer in self.consumers:
#            self.logger.warning('consumer already registered: consumer=%s', consumer)
#
#        else:
 #           self.consumers.append(consumer)
#
#        await self.setup()

#    @coroutine
 #   def remove_consumer(self, consumer):
  #      if consumer not in self.consumers:
   #         self.logger.warning('unknown consumer: consumer=%s', consumer)
#
#            return

#        self.consumers.remove(consumer)

 #       if not self.consumers:
  #          await self.shutdown()

    async def setup(self):
        if self.pending_initialization is not None:
            self.logger.debug('previous initialization already running')
            await self.pending_initialization
            return

        self.logger.debug('starting initialization')

        self.pending_initialization = Future()

        if self.pending_shutdown is not None:
            self.logger.debug('waiting for a previous running shutdown to be complete')
            # if a shutdown is running, let's wait it to be completed before
            # starting a setup again
            await self.pending_shutdown

            self.logger.debug('shutdown complete, starting setup')

        channel = await self.exchange.client.ensure_connected()

        self.logger.debug('binding %s to %s with %s',
                          self.exchange, self.exchange.client.queue_name, self.routing_key_pattern)

        await bind_queue(
            channel,
            self.exchange.client.queue_name,
            self.exchange.exchange,
            self.routing_key_pattern
        )

        self.logger.debug('queue bound')

        # Add a callback that will be invoked if RabbitMQ cancels the consumer
        # for some reason. If RabbitMQ does cancel the consumer,
        # on_consumer_cancelled will be invoked by pika.
        self.logger.debug('adding consumer cancellation callback')

        channel.add_on_cancel_callback(self.on_consumer_cancelled)

        self.logger.info('start consuming')

        self._consumer_tag = channel.basic_consume(
            self.exchange.client.queue_name,
            on_message_callback=self.on_message,
        )

        self.logger.debug('initialization complete')

        self.pending_initialization.set_result(None)

    async def shutdown(self):
        if self.pending_initialization is None:
            self.logger.debug('noop shutdown, subscription not initialized')
            return

        if self.pending_shutdown is not None:
            self.logger.debug('shutdown already running, nothing to do')
            # await self.pending_shutdown # no need to wait
            return

        self.logger.debug('shutdown sequence starting')

        self.pending_shutdown = Future()

        if self.pending_initialization is not None:
            self.logger.debug('waiting for a previous started initialization to be completed')

            # if a initialization is running, let's wait it to be completed before
            # shutting everything down
            await self.pending_initialization

            self.pending_initialization = None

            self.logger.debug('initialization complete, now starting shutdown')

        # don't know how to remove a callback...

        channel = self.exchange.client.ensure_connected()

        self.logger.debug('cancelling consume: tag=%s', self._consumer_tag)

        await basic_cancel(channel, self._consumer_tag)

        self.logger.debug('unbinding queue')

        await unbind_queue(channel, self.exchange.client.queue_name, self.exchange.exchange, self.routing_key_pattern)

        self.logger.info('shutdown complete')

        self.pending_shutdown.set_result(None)
        self.pending_shutdown = None

    async def rebind_after_reconnection(self):
        self.pending_initialization = None

        await self.setup()

    def on_consumer_cancelled(self, method_frame):
        """Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
        receiving messages.

        :param pika.frame.Method method_frame: The Basic.Cancel frame

        """
        self.logger.info('consumer was cancelled remotely, shutting down: %r', method_frame)

        if self.pending_shutdown is not None:
            return

        # TODO: what to do? if self._channel:
        #    self._channel.close()

    def on_message(self, channel: Channel, basic_deliver, properties, body: Message):
        """Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.

        :param pika.channel.Channel unused_channel: The channel object
        :param pika.Spec.Basic.Deliver basic_deliver: basic_deliver method
        :param pika.Spec.BasicProperties properties: properties
        :param bytes body: The message body

        """
        self.logger.debug('received message # %s from %s topic=%s: %s',
                          basic_deliver.delivery_tag, properties.app_id, basic_deliver.routing_key, body)

        self.acknowledge_message(channel, basic_deliver.delivery_tag)

        try:
            self.consumer(basic_deliver.routing_key, body)
        except Exception as e:
            self.logger.error('message delivery failed: consumer=%s, cause=%s, message=%s', self.consumer, e, body)

    def acknowledge_message(self, channel: Channel, delivery_tag):
        """Acknowledge the message delivery from RabbitMQ by sending a
        Basic.Ack RPC method for the delivery tag.

        :param int delivery_tag: The delivery tag from the Basic.Deliver frame

        """
        self.logger.info('Acknowledging message %s', delivery_tag)

        channel.basic_ack(delivery_tag)

    def __str__(self):
        return '%s=%s' % (self.exchange.exchange, self.routing_key_pattern)
