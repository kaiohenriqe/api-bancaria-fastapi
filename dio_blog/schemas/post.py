from datetime import datetime
from pydantic import BaseModel

class PostBase(BaseModel):
    titulo: str
    conteudo: str

class PostIn(PostBase):
    pass

class PostOut(PostBase):
    id: int
    date: datetime

    class Config:
        from_attributes = True
