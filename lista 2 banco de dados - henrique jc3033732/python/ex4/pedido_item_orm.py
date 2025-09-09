from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Pedido(Base):
    __tablename__ = 'pedido'
    id = Column(Integer, primary_key=True)
    data = Column(String(45))

    itens = relationship("Item",
                            secondary="pedido_item_table",
                            back_populates="pedidos")

    def __repr__(self):
        return f"<Pedido(id={self.id}, data='{self.data}')>"