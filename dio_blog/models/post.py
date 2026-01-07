from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from dio_blog.database import Base

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    titulo: Mapped[str] = mapped_column(sa.String, nullable=False)
    conteudo: Mapped[str] = mapped_column(sa.Text, nullable=False)
    date: Mapped[datetime] = mapped_column(sa.DateTime, default=sa.func.now())