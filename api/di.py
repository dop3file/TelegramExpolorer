from elasticsearch import AsyncElasticsearch

from TelegramExpolorer.api.post_service import PostService
from TelegramExpolorer.common.config import config
from TelegramExpolorer.common.db.session import DBSession
from TelegramExpolorer.common.indexer import Indexer


class DIContainer:
    def __init__(self, indexer: Indexer, post_service: PostService):
        self.indexer = indexer
        self.post_service = post_service


di_container = DIContainer(
    Indexer(AsyncElasticsearch(["http://localhost:9200"]), "posts"),
    PostService(
        DBSession(config.POSTGRES_DB_CONNECTOR),
    ),
)
