from pydantic import BaseModel


class Post(BaseModel):
    id: int
    text: str
