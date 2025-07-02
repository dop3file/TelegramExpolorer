from fastapi import APIRouter

from TelegramExpolorer.api.schemas import Post
from TelegramExpolorer.api.di import di_container

router = APIRouter()


@router.get("/search")
async def search(query: str) -> list[Post]:
    post_ids = await di_container.indexer.search(query)
    return await di_container.post_service.get_posts(post_ids)
