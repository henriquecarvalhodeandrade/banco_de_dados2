from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, timedelta

from classes_biblioteca import (
    Base, Autor, Livro, Dissertacao, Tese,
    Exemplar, Aluno, Emprestimo
)

def popular_dados_iniciais(session):
    autor1 = Autor(nome="Autor A")
    autor2 = Autor(nome="Autor B")
    autor3 = Autor(nome="Autor C")

    livro1 = Livro(titulo="Python para Iniciantes", ano_publicacao=2023, edicao="1ª Edição", autores=[autor1])
    livro2 = Livro(titulo="Banco de Dados Avançado", ano_publicacao=2022, edicao="2ª Edição", autores=[autor2])
    livro3 = Livro(titulo="Estruturas de Dados em C++", ano_publicacao=2021, edicao="3ª Edição", autores=[autor1, autor2])
    dissertacao1 = Dissertacao(titulo="IA e o Futuro", ano_publicacao=2024, programa_pos="Ciência da Computação", autores=[autor2])
    tese1 = Tese(titulo="Redes Neurais Profundas", ano_publicacao=2020, programa_pos="Inteligência Artificial", autores=[autor1])
    livro4 = Livro(titulo="Machine Learning com Python", ano_publicacao=2023, edicao="1ª Edição", autores=[autor3])
    livro5 = Livro(titulo="Introdução à Programação em C", ano_publicacao=2019, edicao="4ª Edição", autores=[autor1])
    dissertacao2 = Dissertacao(titulo="Big Data na Saúde", ano_publicacao=2022, programa_pos="Engenharia Biomédica", autores=[autor2])
    tese2 = Tese(titulo="Algoritmos Quânticos", ano_publicacao=2021, programa_pos="Computação Quântica", autores=[autor3])
    livro6 = Livro(titulo="Engenharia de Software Moderna", ano_publicacao=2020, edicao="2ª Edição", autores=[autor1, autor3])

    exemplares = [
        Exemplar(material=livro1, disponivel=1),
        Exemplar(material=livro2, disponivel=1),
        Exemplar(material=livro3, disponivel=1),
        Exemplar(material=dissertacao1, disponivel=1),
        Exemplar(material=tese1, disponivel=1),
        Exemplar(material=livro4, disponivel=1),
        Exemplar(material=livro5, disponivel=1),
        Exemplar(material=dissertacao2, disponivel=1),
        Exemplar(material=tese2, disponivel=1),
        Exemplar(material=livro6, disponivel=1),
    ]

    aluno1 = Aluno(nome="João Silva", matricula="123456", curso="Engenharia")

    session.add_all([
        autor1, autor2, autor3,
        livro1, livro2, livro3, dissertacao1, tese1,
        livro4, livro5, dissertacao2, tese2, livro6,
        aluno1
    ] + exemplares)
    session.commit()

    hoje = date.today()

    emprestimos = [
        Emprestimo(usuario=aluno1, exemplar=exemplares[5], data_emprestimo=hoje),
        Emprestimo(usuario=aluno1, exemplar=exemplares[6], data_emprestimo=hoje - timedelta(days=2)), 
        Emprestimo(usuario=aluno1, exemplar=exemplares[7], data_emprestimo=hoje - timedelta(days=5)),
        Emprestimo(usuario=aluno1, exemplar=exemplares[8], data_emprestimo=hoje - timedelta(days=7)), 
        Emprestimo(usuario=aluno1, exemplar=exemplares[9], data_emprestimo=hoje - timedelta(days=10)), 
    ]
    
    # 📚 Adiciona o loop para atualizar a disponibilidade
    for emp in emprestimos:
        emp.exemplar.disponivel = 0

    session.add_all(emprestimos)
    session.commit()

    # Opcional: Remova o for loop que apenas printa informações se desejar.

def setup_test_db():
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_HOST = 'localhost'
    MYSQL_DB_TEST = 'biblioteca_universitaria_teste'

    engine = create_engine(f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB_TEST}')
    
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    return session, engine

if __name__ == "__main__":
    print("--- Populando o banco com exemplos ---")
    session, engine = setup_test_db()
    popular_dados_iniciais(session)
    print("\n Banco de dados populado com sucesso!")
    session.close()
