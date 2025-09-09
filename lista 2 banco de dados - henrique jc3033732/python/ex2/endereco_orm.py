from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Endereco(Base):
    __tablename__ = 'endereco'
    id = Column(Integer, primary_key=True)
    rua = Column(String(100))
    numero = Column(String(10))
    cliente_id = Column(Integer, ForeignKey('cliente.id'))

    cliente = relationship("Cliente", back_populates="endereco")

    def __repr__(self):
        return f"<Endereco(rua='{self.rua}', numero='{self.numero}')>"