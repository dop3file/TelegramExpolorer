import asyncio

from aio_pika import connect
from telethon import TelegramClient

from TelegramExpolorer.crawler.config import config
from TelegramExpolorer.crawler.consumer import Consumer, ChatHandler


async def main():
    consumer = Consumer(
        await connect(config.RABBIT_MQ_URL), queue_name=config.CHANNELS_QUEUE_NAME
    )
    await consumer.consume(ChatHandler())


asyncio.run(main())
