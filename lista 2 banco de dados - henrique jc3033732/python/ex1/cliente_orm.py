from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'cliente'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    endereco = Column(String(200))

    def __repr__(self):
        return f"<Cliente(id={self.id}, nome='{self.nome}', endereco='{self.endereco}')>"

DATABASE_URL = "mysql+mysqlconnector://<user>:<password>@<host>/<database>"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine) 
Session = sessionmaker(bind=engine)
session = Session()

if __name__ == '__main__':
    print("Módulo de mapeamento Cliente OK.")
    novo_cliente = Cliente(nome="João da Silva", endereco="Rua A, 123")
    session.add(novo_cliente)
    session.commit()
    print("Cliente adicionado com sucesso!")

    clientes = session.query(Cliente).all()
    for cliente in clientes:
        print(cliente)
    
    session.close()