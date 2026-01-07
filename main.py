from fastapi import FastAPI
from dio_blog.controllers import post
from dio_blog.database import Base, engine
from dio_blog.models.post import Post  # type: ignore
from sqlalchemy.orm import sessionmaker

# Cria as tabelas no banco (uma vez só)
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()
app.include_router(post.router)