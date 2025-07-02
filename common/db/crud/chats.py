from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from TelegramExpolorer.common.db.models import ChatDB
from TelegramExpolorer.common.domain import Chat


async def exists(session: AsyncSession, chat: Chat) -> bool:
    stmt = select(ChatDB).where(ChatDB.id == chat.id)
    result = await session.execute(stmt)
    return result.first() is not None


async def add(session: AsyncSession, chat: Chat) -> None:
    stmt = insert(ChatDB).values(id=chat.id, title=chat.title)
    result = await session.execute(stmt)


async def get_by_id(session: AsyncSession, chat_id: int) -> ChatDB | None:
    stmt = select(ChatDB).where(ChatDB.id == chat_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
