import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship
from dio_blog.database import Base
from datetime import datetime

class ContaCorrente(Base):
    __tablename__ = "contas_correntes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    titular: Mapped[str] = mapped_column(sa.String(200), nullable=False)
    saldo: Mapped[float] = mapped_column(sa.Float, default=0.0)

    transacoes: Mapped[list["Transacao"]] = relationship("Transacao", back_populates="conta")


class Transacao(Base):
    __tablename__ = "transacoes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    conta_id: Mapped[int] = mapped_column(sa.ForeignKey("contas_correntes.id"))
    tipo: Mapped[str] = mapped_column(sa.String(20), nullable=False)  # "deposito" ou "saque"
    valor: Mapped[float] = mapped_column(sa.Float, nullable=False)
    data: Mapped[datetime] = mapped_column(sa.DateTime(timezone=True), server_default=sa.func.now())

    conta: Mapped["ContaCorrente"] = relationship("ContaCorrente", back_populates="transacoes")
