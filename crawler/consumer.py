import asyncio
import json
from typing import Protocol, Awaitable

from aio_pika import connect, IncomingMessage
from aio_pika.abc import AbstractConnection

from TelegramExpolorer.common.domain import Chat
from TelegramExpolorer.crawler.telegram import parse_chat


class BaseHandler(Protocol):
    def __call__(self, message: IncomingMessage) -> Awaitable: ...


class ChatHandler(BaseHandler):
    async def __call__(self, message: IncomingMessage):
        async with message.process():
            chat = Chat(**json.loads(message.body.decode()))
            await asyncio.create_task(parse_chat(chat))


class Consumer:
    def __init__(self, connection: AbstractConnection, queue_name: str):
        self.connection = connection
        self.queue_name = queue_name

    async def consume(self, message_handler: BaseHandler):
        channel = await self.connection.channel()
        queue = await channel.declare_queue(self.queue_name, durable=True)

        await queue.consume(message_handler)
        await asyncio.Future()
