# app.py

import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from classes_biblioteca import Base, Aluno, Professor, Funcionario, Exemplar, Emprestimo, Reserva
from regras_negocio import realizar_emprestimo, devolver_material, reservar_material, pagar_multa
from tests import popular_dados_iniciais
import pandas as pd

# --- Configuração do Banco de Dados ---
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root123'
MYSQL_HOST = 'localhost'
MYSQL_DB = 'biblioteca_universitaria_teste'

# Usando o cache do Streamlit para a conexão com o banco
@st.cache_resource
def get_engine():
    return create_engine(f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}')

@st.cache_resource
def setup_database(_engine):
    Base.metadata.drop_all(_engine)
    Base.metadata.create_all(_engine)
    Session = sessionmaker(bind=_engine)
    session = Session()
    popular_dados_iniciais(session)
    session.close()

# --- Funções da Interface ---

def listar_usuarios(session):
    st.subheader("Lista de Usuários")
    usuarios = session.query(Aluno).all() + session.query(Professor).all() + session.query(Funcionario).all()
    if usuarios:
        df = pd.DataFrame([(u.id, u.nome, u.tipo) for u in usuarios], columns=['ID', 'Nome', 'Tipo'])
        st.dataframe(df)
    else:
        st.write("Nenhum usuário cadastrado.")

def listar_exemplares(session):
    st.subheader("Lista de Exemplares")
    exemplares = session.query(Exemplar).all()
    if exemplares:
        data = []
        for e in exemplares:
            status = "Disponível" if e.disponivel == 1 else "Indisponível"
            data.append((e.id, e.material.titulo, status))
        df = pd.DataFrame(data, columns=['ID', 'Material', 'Status'])
        st.dataframe(df)
    else:
        st.write("Nenhum exemplar cadastrado.")

def listar_emprestimos(session):
    st.subheader("Lista de Empréstimos")
    emprestimos = session.query(Emprestimo).all()
    if not emprestimos:
        st.write("Não há empréstimos registrados.")
        return
    
    data = []
    for emp in emprestimos:
        emp.calcular_multa() # Calcula a multa em tempo real
        session.commit()
        status = "Devolvido" if emp.data_devolucao else "Em andamento"
        multa_info = f"R$ {emp.multa:.2f}" if emp.multa > 0 else "R$ 0.00"
        data.append((
            emp.id, 
            emp.usuario.nome, 
            emp.exemplar.material.titulo, 
            emp.data_emprestimo, 
            status, 
            multa_info
        ))
    df = pd.DataFrame(data, columns=['ID', 'Usuário', 'Título', 'Data Empréstimo', 'Status', 'Multa'])
    st.dataframe(df)


def listar_reservas(session):
    st.subheader("Lista de Reservas")
    reservas = session.query(Reserva).all()
    if not reservas:
        st.write("Não há reservas registradas.")
        return
    
    data = [(res.id, res.usuario.nome, res.exemplar.material.titulo, res.data_reserva) for res in reservas]
    df = pd.DataFrame(data, columns=['ID', 'Usuário', 'Exemplar', 'Data da Reserva'])
    st.dataframe(df)

# --- Aplicação Principal ---

def main():
    st.title("Sistema de Gerenciamento de Biblioteca")

    engine = get_engine()
    # Botão para (re)popular o banco de dados
    if st.sidebar.button("Resetar e Popular Banco de Dados"):
        setup_database(engine)
        st.sidebar.success("Banco de dados resetado e populado com sucesso!")

    Session = sessionmaker(bind=engine)
    session = Session()

    st.sidebar.title("Menu")
    opcao = st.sidebar.radio("Escolha uma operação:", 
                             ["Visualizar Listas", "Realizar Empréstimo", "Devolver Material", "Reservar Material", "Pagar Multa"])

    if opcao == "Visualizar Listas":
        tipo_lista = st.selectbox("Selecione a lista que deseja visualizar:", 
                                  ["Usuários", "Exemplares", "Empréstimos", "Reservas"])
        if tipo_lista == "Usuários":
            listar_usuarios(session)
        elif tipo_lista == "Exemplares":
            listar_exemplares(session)
        elif tipo_lista == "Empréstimos":
            listar_emprestimos(session)
        elif tipo_lista == "Reservas":
            listar_reservas(session)

    elif opcao == "Realizar Empréstimo":
        st.subheader("Realizar Novo Empréstimo")
        usuario_id = st.number_input("ID do Usuário:", min_value=1, step=1)
        exemplar_id = st.number_input("ID do Exemplar:", min_value=1, step=1)
        if st.button("Emprestar"):
            usuario = session.get(Aluno, usuario_id) or session.get(Professor, usuario_id) or session.get(Funcionario, usuario_id)
            exemplar = session.get(Exemplar, exemplar_id)
            if not usuario:
                st.error("Erro: Usuário não encontrado.")
            elif not exemplar:
                st.error("Erro: Exemplar não encontrado.")
            else:
                sucesso, mensagem = realizar_emprestimo(usuario, exemplar, session)
                if sucesso:
                    st.success(mensagem)
                else:
                    st.error(mensagem)

    elif opcao == "Devolver Material":
        st.subheader("Devolver Material Emprestado")
        emprestimo_id = st.number_input("ID do Empréstimo:", min_value=1, step=1)
        if st.button("Devolver"):
            sucesso, mensagem = devolver_material(emprestimo_id, session)
            if sucesso:
                st.success(mensagem)
            else:
                st.error(mensagem)

    elif opcao == "Reservar Material":
        st.subheader("Reservar Material")
        usuario_id = st.number_input("ID do Usuário para Reserva:", min_value=1, step=1)
        exemplar_id = st.number_input("ID do Exemplar para Reserva:", min_value=1, step=1)
        if st.button("Reservar"):
            usuario = session.get(Aluno, usuario_id) or session.get(Professor, usuario_id) or session.get(Funcionario, usuario_id)
            exemplar = session.get(Exemplar, exemplar_id)
            if not usuario:
                st.error("Erro: Usuário não encontrado.")
            elif not exemplar:
                st.error("Erro: Exemplar não encontrado.")
            else:
                sucesso, mensagem = reservar_material(usuario, exemplar, session)
                if sucesso:
                    st.success(mensagem)
                else:
                    st.error(mensagem)

    elif opcao == "Pagar Multa":
        st.subheader("Pagar Multa de Empréstimo")
        emprestimo_id_multa = st.number_input("ID do Empréstimo com Multa:", min_value=1, step=1)
        if st.button("Pagar Multa"):
            sucesso, mensagem = pagar_multa(emprestimo_id_multa, session)
            if sucesso:
                st.success(mensagem)
            else:
                st.error(mensagem)

    session.close()

main()
