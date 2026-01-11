from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dio_blog.database import SessionLocal
from dio_blog.models import ContaCorrente, Transacao
from auth import verificar_token
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Dependência para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Schemas Pydantic
class TransacaoResponse(BaseModel):
    id: int
    conta_id: int
    tipo: str
    valor: float

    model_config = {"from_attributes": True}

class ExtratoResponse(BaseModel):
    conta_id: int
    titular: str
    saldo: float
    transacoes: List[TransacaoResponse]

    model_config = {"from_attributes": True}

# Endpoints
@router.post("/transacoes", response_model=TransacaoResponse)
async def criar_transacao(
    conta_id: int,
    tipo: str,
    valor: float,
    usuario: str = Depends(verificar_token),
    db: Session = Depends(get_db)
) -> TransacaoResponse: 
    if valor <= 0:
        raise HTTPException(status_code=400, detail="Valor deve ser positivo")

    conta = db.query(ContaCorrente).filter(ContaCorrente.id == conta_id).first()
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    if tipo == "deposito":
        conta.saldo += valor
    elif tipo == "saque":
        if conta.saldo < valor:
            raise HTTPException(status_code=400, detail="Saldo insuficiente")
        conta.saldo -= valor
    else:
        raise HTTPException(status_code=400, detail="Tipo de transação inválido")

    transacao = Transacao(conta_id=conta.id, tipo=tipo, valor=valor)
    db.add(transacao)
    db.commit()
    db.refresh(transacao)

    return TransacaoResponse.model_validate(transacao)

@router.get("/extrato/{conta_id}", response_model=ExtratoResponse)
async def extrato(
    conta_id: int,
    usuario: str = Depends(verificar_token),
    db: Session = Depends(get_db)
) -> ExtratoResponse:
    conta = db.query(ContaCorrente).filter(ContaCorrente.id == conta_id).first()
    if not conta:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    transacoes_db = db.query(Transacao).filter(Transacao.conta_id == conta_id).all()
    transacoes_resp = [TransacaoResponse.model_validate(t) for t in transacoes_db]

    return ExtratoResponse(
        conta_id=conta.id,
        titular=conta.titular,
        saldo=conta.saldo,
        transacoes=transacoes_resp
    )