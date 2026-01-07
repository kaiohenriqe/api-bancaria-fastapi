from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from dio_blog.database import SessionLocal
from dio_blog.models.post import Post
from dio_blog.schemas.post import PostIn, PostOut

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PostOut, status_code=status.HTTP_201_CREATED)
def criar_post(post: PostIn, db: Session = Depends(get_db)):
    novo_post = Post(titulo=post.titulo, conteudo=post.conteudo)
    db.add(novo_post)
    db.commit()
    db.refresh(novo_post)
    return novo_post


@router.get("/", response_model=List[PostOut])
def listar_posts(db: Session = Depends(get_db)):
    return db.query(Post).all()


@router.get("/{post_id}", response_model=PostOut)
def obter_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post não encontrado")
    return post


@router.put("/{post_id}", response_model=PostOut)
def atualizar_post(post_id: int, post: PostIn, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post não encontrado")
    db_post.titulo = post.titulo
    db_post.conteudo = post.conteudo
    db.commit()
    db.refresh(db_post)
    return db_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post não encontrado")
    db.delete(db_post)
    db.commit()