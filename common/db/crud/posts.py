from datetime import datetime
from typing import Sequence

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from TelegramExpolorer.common.db.models import PostDB
from TelegramExpolorer.common.domain import Post


async def add(session: AsyncSession, post: Post) -> None:
    stmt = insert(PostDB).values(
        id=post.id,
        text=post.text,
        chat_id=post.chat,
        create_date=datetime.fromtimestamp(post.created_at),
        link=post.link,
    )
    await session.execute(stmt)


async def get_by_ids(session: AsyncSession, ids: list[int]) -> Sequence[PostDB]:
    stmt = select(PostDB).where(PostDB.id.in_(ids))
    result = await session.execute(stmt)
    return result.scalars().all()
