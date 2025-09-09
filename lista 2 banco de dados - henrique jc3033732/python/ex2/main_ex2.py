from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cliente_endereco_orm import Base, Cliente
from endereco_orm import Endereco

DATABASE_URL = "mysql+mysqlconnector://<user>:<password>@<host>/<database>"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

novo_cliente = Cliente(nome="Maria Oliveira")
novo_endereco = Endereco(rua="Rua B", numero="456")
novo_cliente.endereco = novo_endereco 

session.add(novo_cliente)
session.commit()
print("Cliente e endereço adicionados com sucesso!")

cliente_buscado = session.query(Cliente).filter_by(nome="Maria Oliveira").first()
print(f"Cliente: {cliente_buscado.nome}")
print(f"Endereço: {cliente_buscado.endereco.rua}, {cliente_buscado.endereco.numero}")

session.close()