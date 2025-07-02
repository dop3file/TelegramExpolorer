import asyncio
from aio_pika import connect, Message, DeliveryMode, ExchangeType
from aio_pika.abc import AbstractConnection, AbstractChannel


class Producer:
    def __init__(self, channel: AbstractChannel, queue_name: str):
        self._channel = channel
        self._queue_name = queue_name

    async def publish(self, message_body: str):
        queue = await self._channel.declare_queue(self._queue_name, durable=True)

        message = Message(
            body=message_body.encode("utf-8"),
            delivery_mode=DeliveryMode.PERSISTENT,
        )
        await self._channel.default_exchange.publish(message, routing_key=queue.name)
