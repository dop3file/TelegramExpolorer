import asyncio

from aio_pika import connect
from telethon import TelegramClient

from TelegramExpolorer.common.db.session import DBSession
from TelegramExpolorer.common.config import config
from TelegramExpolorer.common.queue.consumer import Consumer
from TelegramExpolorer.common.queue.producer import Producer
from TelegramExpolorer.crawler.handler import ChatHandler
from TelegramExpolorer.crawler.misc import keep_alive


async def main():
    async with TelegramClient(
        "anon", config.TELEGRAM_APP_ID, config.TELEGRAM_APP_HASH
    ) as client:
        asyncio.create_task(keep_alive(client))
        connection = await connect(config.RABBIT_MQ_URL)
        post_channel = await connection.channel()
        channel_channel = await connection.channel()
        db_session = DBSession(config.POSTGRES_DB_CONNECTOR)
        try:
            post_producer = Producer(post_channel, queue_name=config.POSTS_QUEUE_NAME)
            channel_producer = Producer(
                channel_channel, queue_name=config.CHANNELS_QUEUE_NAME
            )
            channel_consumer = Consumer(
                channel_channel, queue_name=config.CHANNELS_QUEUE_NAME
            )
            await channel_consumer.consume(
                ChatHandler(client, post_producer, channel_producer, db_session)
            )
        finally:
            await connection.close()


asyncio.run(main())
