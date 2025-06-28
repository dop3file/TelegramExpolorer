from dataclasses import dataclass

from envparse import env


@dataclass
class Config:
    TELEGRAM_APP_ID: int = env.int("TELEGRAM_APP_ID")
    TELEGRAM_APP_HASH: str = env.str("TELEGRAM_APP_HASH")

    CHANNELS_QUEUE_NAME: str = env.str("CHANNELS_QUEUE_NAME")
    POSTS_QUEUE_NAME: str = env.str("POSTS_QUEUE_NAME")

    RABBIT_MQ_URL: str = env.str("RABBIT_MQ_URL")


config = Config()
