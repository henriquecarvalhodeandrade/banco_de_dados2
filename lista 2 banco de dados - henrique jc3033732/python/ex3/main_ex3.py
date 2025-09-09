from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cliente_pedido_orm import Base, Cliente
from pedido_orm import Pedido

DATABASE_URL = "mysql+mysqlconnector://<user>:<password>@<host>/<database>"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Exemplo de uso:
cliente1 = Cliente(nome="Carlos Souza")
pedido1 = Pedido(data="2023-08-25", total=50.00)
pedido2 = Pedido(data="2023-08-26", total=75.50)

cliente1.pedidos.append(pedido1) 
cliente1.pedidos.append(pedido2)

session.add(cliente1)
session.commit()
print("Cliente e pedidos adicionados com sucesso!")

cliente_buscado = session.query(Cliente).filter_by(nome="Carlos Souza").first()
print(f"Pedidos de {cliente_buscado.nome}:")
for pedido in cliente_buscado.pedidos:
    print(f"  - Pedido ID: {pedido.id}, Total: {pedido.total}")

session.close()