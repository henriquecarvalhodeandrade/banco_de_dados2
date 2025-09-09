from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Pedido(Base):
    __tablename__ = 'pedido'
    id = Column(Integer, primary_key=True)
    data = Column(String(45))
    total = Column(Float)
    cliente_id = Column(Integer, ForeignKey('cliente.id'))

    cliente = relationship("Cliente", back_populates="pedidos")

    def __repr__(self):
        return f"<Pedido(id={self.id}, data='{self.data}', total={self.total})>"