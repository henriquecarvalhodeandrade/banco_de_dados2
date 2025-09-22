from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from classes_biblioteca import Base, Aluno, Professor, Funcionario, Exemplar, Emprestimo, Reserva
from regras_negocio import realizar_emprestimo, devolver_material, reservar_material
from tests import popular_dados_iniciais

MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_HOST = 'localhost'
MYSQL_DB = 'biblioteca_universitaria_teste'

def listar_usuarios(session):
    usuarios = session.query(Aluno).all() + session.query(Professor).all() + session.query(Funcionario).all()
    for u in usuarios:
        print(f"ID: {u.id} | Nome: {u.nome} | Tipo: {u.tipo}")

def listar_exemplares(session):
    exemplares = session.query(Exemplar).all()
    for e in exemplares:
        status = "Disponível" if e.disponivel == 1 else "Indisponível"
        print(f"ID: {e.id} | Material: {e.material.titulo} | Status: {status}")

def listar_emprestimos(session):
    emprestimos = session.query(Emprestimo).all()
    if not emprestimos:
        print("Não há empréstimos registrados.")
        return
    for emp in emprestimos:
        status = "Devolvido" if emp.data_devolucao else "Em andamento"
        multa_info = f", Multa: R$ {emp.multa:.2f}" if emp.multa > 0 else ""
        print(f"ID: {emp.id} | Usuário: {emp.usuario.nome} | Exemplar ID: {emp.exemplar.id} | Título: {emp.exemplar.material.titulo} | Data Empréstimo: {emp.data_emprestimo} | Status: {status}{multa_info}")

def listar_reservas(session):
    reservas = session.query(Reserva).all()
    if not reservas:
        print("Não há reservas registradas.")
        return
    for res in reservas:
        print(f"ID: {res.id} | Usuário: {res.usuario.nome} | Exemplar: {res.exemplar.material.titulo} | Data da Reserva: {res.data_reserva}")

def menu(session):
    while True:
        print("\n=== Sistema de Biblioteca ===")
        print("1. Listar usuários")
        print("2. Listar exemplares")
        print("3. Listar empréstimos")
        print("4. Listar reservas")
        print("5. Realizar empréstimo")
        print("6. Devolver material")
        print("7. Reservar material")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            listar_usuarios(session)
        elif opcao == "2":
            listar_exemplares(session)
        elif opcao == "3":
            listar_emprestimos(session)
        elif opcao == "4":
            listar_reservas(session)
        elif opcao == "5":
            usuario_id = int(input("ID do usuário: "))
            exemplar_id = int(input("ID do exemplar: "))
            usuario = session.get(Aluno, usuario_id) or session.get(Professor, usuario_id) or session.get(Funcionario, usuario_id)
            exemplar = session.get(Exemplar, exemplar_id)
            if not usuario:
                print("Erro: Usuário não encontrado.")
            elif not exemplar:
                print("Erro: Exemplar não encontrado.")
            else:
                sucesso, mensagem = realizar_emprestimo(usuario, exemplar, session)
                print(mensagem)
        elif opcao == "6":
            emprestimo_id = int(input("ID do empréstimo: "))
            sucesso, mensagem = devolver_material(emprestimo_id, session)
            print(mensagem)
        elif opcao == "7":
            usuario_id = int(input("ID do usuário: "))
            exemplar_id = int(input("ID do exemplar: "))
            usuario = session.get(Aluno, usuario_id) or session.get(Professor, usuario_id) or session.get(Funcionario, usuario_id)
            exemplar = session.get(Exemplar, exemplar_id)
            if not usuario:
                print("Erro: Usuário não encontrado.")
            elif not exemplar:
                print("Erro: Exemplar não encontrado.")
            else:
                sucesso, mensagem = reservar_material(usuario, exemplar, session)
                print(mensagem)
        elif opcao == "0":
            print("Saindo do sistema...")
            session.close()
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    engine = create_engine(f'mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    print("Sistema de Gerenciamento de Biblioteca")
    print("Conectado ao banco de dados MySQL.")
    popular_dados_iniciais(session)

    menu(session)