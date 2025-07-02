import datetime
from dataclasses import dataclass, field


@dataclass
class Chat:
    id: str | int
    title: str | None = field(default=None)


@dataclass
class Post:
    id: int
    chat: int
    text: str
    created_at: float
    link: str
