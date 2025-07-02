import asyncio

from aio_pika import connect

from TelegramExpolorer.common.config import config
from TelegramExpolorer.common.db.session import DBSession
from TelegramExpolorer.common.queue.consumer import Consumer
from TelegramExpolorer.parser.handler import PostHandler
from TelegramExpolorer.common.indexer import Indexer

from elasticsearch import AsyncElasticsearch


async def main():
    db_session = DBSession(db_url=config.POSTGRES_DB_CONNECTOR)
    connection = await connect(config.RABBIT_MQ_URL)
    indexer = Indexer(AsyncElasticsearch(["http://localhost:9200"]), "posts")
    post_channel = await connection.channel()
    try:
        post_consumer = Consumer(post_channel, queue_name=config.POSTS_QUEUE_NAME)
        await post_consumer.consume(PostHandler(db_session, indexer))
    finally:
        await connection.close()


if __name__ == "__main__":
    asyncio.run(main())
