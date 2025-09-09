from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'cliente'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100))

    endereco = relationship("Endereco", back_populates="cliente", uselist=False)

    def __repr__(self):
        return f"<Cliente(nome='{self.nome}')>"