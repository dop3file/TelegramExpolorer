import asyncio
import re

from telethon import TelegramClient


def get_links_from_post(text: str) -> list[str]:
    result = re.findall(r"(?:^|\s)@([a-zA-Z0-9_]{5,32})(?=\s|$)", text)
    return result


async def keep_alive(client: TelegramClient) -> None:
    while True:
        if not client.is_connected():
            await client.connect()
        await asyncio.sleep(10)
