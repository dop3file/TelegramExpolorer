from TelegramExpolorer.api.schemas import Post
from TelegramExpolorer.common.db.session import DBSession

from TelegramExpolorer.common.db.crud import posts as db_posts


class PostService:
    def __init__(self, db_session: DBSession):
        self._db_session = db_session

    async def get_posts(self, ids: list[int]) -> list[Post]:
        async with self._db_session.async_session() as session:
            return [
                Post(id=post.id, text=post.text)
                for post in await db_posts.get_by_ids(session, ids)
            ]
