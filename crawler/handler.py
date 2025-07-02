import asyncio
import json
from asyncio import gather
from dataclasses import asdict

from aio_pika import IncomingMessage
from loguru import logger
from telethon import TelegramClient
from telethon.tl.types import Channel

from TelegramExpolorer.common.db.session import DBSession
from TelegramExpolorer.common.domain import Chat, Post
from TelegramExpolorer.common.queue.consumer import BaseHandler
from TelegramExpolorer.common.queue.producer import Producer
from TelegramExpolorer.common.db.crud import chats as db_chats
from TelegramExpolorer.crawler.misc import get_links_from_post


class ChatHandler(BaseHandler):
    def __init__(
        self,
        client: TelegramClient,
        post_producer: Producer,
        channel_producer: Producer,
        db_session: DBSession,
    ) -> None:
        self._client = client
        self._post_producer = post_producer
        self._channel_producer = channel_producer
        self._db_session = db_session

    async def __call__(self, message: IncomingMessage):
        try:
            chat = Chat(**json.loads(message.body.decode()))
            logger.debug(f"Chat {chat}")
            await self._parse_chat(chat)
        except Exception as e:
            await message.nack()
            logger.error(f"Error parsing chat {e}", exc_info=e)

    async def _parse_chat(self, chat: Chat):
        async with (
            asyncio.Lock(),
            self._db_session.async_session() as session,
        ):
            await asyncio.sleep(1)
            entity = await self._client.get_entity(chat.id)
            if await db_chats.exists(session, Chat(id=entity.id, title=entity.title)):
                logger.debug(f"Chat with id {entity.id} already exists")
                return
            await db_chats.add(session, Chat(entity.id, entity.title))
            await session.commit()
            await gather(
                *[
                    self._parse_message(message, entity)
                    async for message in self._client.iter_messages(chat.id)
                ],
            )

    async def _parse_message(self, message, chat_entity):
        await asyncio.sleep(0.2)
        if not message.text:
            return
        post = Post(
            id=message.id,
            text=message.text,
            chat=chat_entity.id,
            created_at=message.date.timestamp(),
            link=f"https://t.me/{chat_entity.title}/{message.id}",
        )
        logger.debug(f"Message {post}")
        await self._post_producer.publish(json.dumps(asdict(post)))
        links = get_links_from_post(message.text)
        for link in links:
            entity = await self._client.get_entity(link)
            if isinstance(entity, Channel) and not entity.megagroup:
                logger.debug(f"Link detect {link}")
                await self._channel_producer.publish(json.dumps(asdict(Chat(id=link))))
