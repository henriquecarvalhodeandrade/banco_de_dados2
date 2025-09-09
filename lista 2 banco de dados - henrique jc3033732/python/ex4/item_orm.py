from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    preco = Column(Float)

    # Relacionamento N:N com a classe Pedido
    pedidos = relationship("Pedido",
                            secondary="pedido_item_table",
                            back_populates="itens")

    def __repr__(self):
        return f"<Item(nome='{self.nome}', preco={self.preco})>"