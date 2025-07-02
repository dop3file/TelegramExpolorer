from dataclasses import dataclass
from datetime import datetime


@dataclass
class PostIndex:
    id: int
    text: str
    chat_name: str
    timestamp: datetime
