import asyncio
from typing import Protocol, Awaitable

from aio_pika import IncomingMessage
from aio_pika.abc import AbstractChannel


class BaseHandler(Protocol):
    def __init__(self, *args, **kwargs) -> None: ...
    def __call__(self, message: IncomingMessage) -> Awaitable: ...


class Consumer:
    def __init__(self, channel: AbstractChannel, queue_name: str):
        self._channel = channel
        self._queue_name = queue_name

    async def consume(self, message_handler: BaseHandler):
        queue = await self._channel.declare_queue(self._queue_name, durable=True)

        await queue.consume(message_handler)
        await asyncio.Future()
