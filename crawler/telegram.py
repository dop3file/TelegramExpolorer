from telethon import TelegramClient

from TelegramExpolorer.common.domain import Chat
from TelegramExpolorer.crawler.config import config


async def parse_chat(chat: Chat):
    async with TelegramClient(
        "anon", config.TELEGRAM_APP_ID, config.TELEGRAM_APP_HASH
    ) as client:
        messages = await client.get_messages(chat.id)

        for message in messages:
            print(f"{message.date}: {message.sender_id} -> {message.text}")
