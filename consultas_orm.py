from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from classes_biblioteca import Livro, Material, Autor, Emprestimo

MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_HOST = 'localhost'
MYSQL_DB = 'biblioteca_universitaria_teste'

engine = create_engine(f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}')
Session = sessionmaker(bind=engine)
session = Session()

try:
    print("--- Executando Consultas com a API do ORM ---")

    # Exemplo 1: Pesquisa por filtros múltiplos
    print("\n## 1. Pesquisa por filtros múltiplos (título e ano)")
    livro_filtrado = session.query(Livro).filter_by(titulo="Machine Learning com Python", ano_publicacao=2023).first()
    if livro_filtrado:
        print(f"Livro encontrado: {livro_filtrado.titulo} ({livro_filtrado.ano_publicacao})")
    else:
        print("Livro não encontrado.")

    # Exemplo 2: Pesquisa por um material com um autor específico 
    print("\n## 2. Pesquisa de materiais por autor")
    autor_alvo = session.query(Autor).filter_by(nome="Autor A").first()
    if autor_alvo:
        materiais_do_autor = autor_alvo.obras
        print(f"Materiais escritos por '{autor_alvo.nome}':")
        for material in materiais_do_autor:
            print(f"  - {material.titulo}")
    else:
        print("Autor não encontrado.")

    # Exemplo 3: Relatório agregado 
    print("\n## 3. Relatório agregado (contagem de empréstimos)")
    total_emprestimos = session.query(func.count(Emprestimo.id)).scalar()
    print(f"Total de empréstimos registrados: {total_emprestimos}")

    # Exemplo 4: Queries com a condição LIKE
    print("\n## 4. Queries com LIKE ('%Dados%')")
    materiais_dados = session.query(Material).filter(Material.titulo.like('%Dados%')).all()
    print("Materiais com a palavra 'Dados' no título:")
    for material in materiais_dados:
        print(f"  - {material.titulo}")

except Exception as e:
    print(f"Ocorreu um erro: {e}")
    session.rollback()

finally:
    session.close()