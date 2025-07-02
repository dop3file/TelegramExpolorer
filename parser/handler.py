import json

from aio_pika import IncomingMessage
from loguru import logger
from sqlalchemy.exc import IntegrityError

from TelegramExpolorer.common.db.session import DBSession
from TelegramExpolorer.common.domain import Post, Chat
from TelegramExpolorer.common.queue.consumer import BaseHandler
from TelegramExpolorer.common.db.crud import posts as db_posts
from TelegramExpolorer.parser.domain import PostIndex
from TelegramExpolorer.common.indexer import Indexer
from TelegramExpolorer.common.db.crud import chats as db_chats


class PostHandler(BaseHandler):
    def __init__(
        self,
        db_session: DBSession,
        indexer: Indexer,
    ) -> None:
        self._db_session = db_session
        self._indexer = indexer

    async def __call__(self, message: IncomingMessage):
        try:
            post = Post(**json.loads(message.body.decode()))
            await self._parse_post(post)
        except Exception as e:
            logger.error(e)
            await message.nack()

    async def _parse_post(self, post: Post) -> None:
        async with self._db_session.async_session() as session:
            try:
                await db_posts.add(session, post)
            except IntegrityError:
                await session.rollback()
                if not await db_chats.exists(session, Chat(id=post.chat)):
                    await db_chats.add(session, Chat(id=post.chat, title=""))
                await db_posts.add(session, post)
            chat = await db_chats.get_by_id(session, post.chat)
            await session.commit()
            await self._indexer.create_post_index(
                PostIndex(
                    id=post.id,
                    text=post.text,
                    chat_name=chat.title,
                    timestamp=post.created_at,
                )
            )
