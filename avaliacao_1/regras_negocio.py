from datetime import date
from classes_biblioteca import Emprestimo, Reserva

LIMITES_EMPRESTIMOS = {
    'aluno': 5,
    'professor': 10,
    'funcionario': 7
}

def pode_emprestar(usuario, session):
    emprestimos_usuario = session.query(Emprestimo).filter(
        Emprestimo.usuario_id == usuario.id
    ).all()

    # Conta os ativos
    emprestimos_ativos = sum(1 for e in emprestimos_usuario if e.data_devolucao is None)
    limite = LIMITES_EMPRESTIMOS.get(usuario.tipo, 0)

    if emprestimos_ativos >= limite:
        return False, f"Limite de empréstimos excedido para {usuario.nome}."

    # Verifica multas em tempo real
    for emp in emprestimos_usuario:
        emp.calcular_multa()
        session.add(emp)
        session.commit()
        if emp.multa > 0:
            return False, f"Usuário {usuario.nome} possui multa pendente e não pode realizar novos empréstimos."

    return True, "Empréstimo permitido."

def realizar_emprestimo(usuario, exemplar, session):
    if exemplar.disponivel == 0:
        return False, "O exemplar não está disponível para empréstimo."
    
    pode, mensagem = pode_emprestar(usuario, session)
    if not pode:
        return False, mensagem
        
    novo_emprestimo = Emprestimo(usuario=usuario, exemplar=exemplar, data_emprestimo=date.today())
    exemplar.disponivel = 0
    session.add(novo_emprestimo)
    session.commit()
    
    return True, f"Empréstimo de '{exemplar.material.titulo}' realizado com sucesso!"

def devolver_material(id_emprestimo, session):
    emprestimo = session.query(Emprestimo).get(id_emprestimo)
    
    if not emprestimo:
        return False, f"Empréstimo com ID {id_emprestimo} não encontrado."
    
    if emprestimo.data_devolucao:
        return False, "Este material já foi devolvido."

    emprestimo.data_devolucao = date.today()
    emprestimo.calcular_multa()
    session.add(emprestimo)
    emprestimo.exemplar.disponivel = 1
    
    session.commit()
    
    multa_info = f"Multa gerada: R$ {emprestimo.multa:.2f}" if emprestimo.multa > 0 else "Nenhuma multa gerada."
    return True, f"Material '{emprestimo.exemplar.material.titulo}' devolvido com sucesso por {emprestimo.usuario.nome}. {multa_info}"

def reservar_material(usuario, exemplar, session):
    if exemplar.disponivel == 1:
        return False, "Este exemplar está disponível e não precisa ser reservado. Realize um empréstimo."

    reserva_existente = session.query(Reserva).filter(
        Reserva.usuario_id == usuario.id,
        Reserva.exemplar_id == exemplar.id
    ).first()

    if reserva_existente:
        return False, f"Usuário {usuario.nome} já possui uma reserva para este exemplar."

    nova_reserva = Reserva(usuario=usuario, exemplar=exemplar, data_reserva=date.today())
    session.add(nova_reserva)
    session.commit()
    return True, "Reserva realizada com sucesso."

def pagar_multa(id_emprestimo, session):
    """
    Paga a multa de um empréstimo, zerando seu valor e atualizando a data de devolução.
    """
    emprestimo = session.query(Emprestimo).get(id_emprestimo)
    
    if not emprestimo:
        return False, f"Empréstimo com ID {id_emprestimo} não encontrado."
    
    if emprestimo.multa == 0:
        return False, "Este empréstimo não possui multa pendente."

    # 📚 Lógica atualizada: Zera a multa, seta a data de devolução e atualiza a disponibilidade
    emprestimo.multa = 0
    emprestimo.data_devolucao = date.today()
    emprestimo.exemplar.disponivel = 1
    session.add(emprestimo)
    session.commit()
    
    return True, f"Multa do empréstimo {id_emprestimo} paga com sucesso. O material foi devolvido e o usuário pode realizar novos empréstimos."