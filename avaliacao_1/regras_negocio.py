from datetime import date
from classes_biblioteca import Emprestimo, Reserva

LIMITES_EMPRESTIMOS = {
    'aluno': 5,
    'professor': 10,
    'funcionario': 7
}

def pode_emprestar(usuario, session):
    emprestimos_ativos = session.query(Emprestimo).filter(
        Emprestimo.usuario_id == usuario.id,
        Emprestimo.data_devolucao.is_(None)
    ).count()

    limite = LIMITES_EMPRESTIMOS.get(usuario.tipo, 0)

    if emprestimos_ativos >= limite:
        return False, f"Limite de empréstimos excedido para {usuario.nome}."

    multa_pendente = session.query(Emprestimo).filter(
        Emprestimo.usuario_id == usuario.id,
        Emprestimo.multa > 0
    ).first()

    if multa_pendente:
        return False, f"Usuário {usuario.nome} possui multa pendente e não pode realizar novos empréstimos."

    return True, "Empréstimo permitido."
    
def realizar_emprestimo(usuario, exemplar, session):
    if exemplar.disponivel == 0:
        return False, "O exemplar não está disponível para empréstimo."
    
    pode, mensagem = pode_emprestar(usuario, session)
    if not pode:
        return False, mensagem
    
    emprestimo = Emprestimo(usuario=usuario, exemplar=exemplar, data_emprestimo=date.today())
    exemplar.disponivel = 0
    session.add(emprestimo)
    session.commit()
    
    return True, f'Empréstimo de "{exemplar.material.titulo}" para {usuario.nome} realizado com sucesso!'

def devolver_material(id_emprestimo, session):
    emprestimo = session.query(Emprestimo).get(id_emprestimo)
    
    if not emprestimo:
        return False, f"Empréstimo com ID {id_emprestimo} não encontrado."
    
    if emprestimo.data_devolucao:
        return False, "Este material já foi devolvido."

    emprestimo.data_devolucao = date.today()
    emprestimo.calcular_multa()
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
        return False, "Você já tem uma reserva para este exemplar."
    
    reserva = Reserva(usuario=usuario, exemplar=exemplar, data_reserva=date.today())
    session.add(reserva)
    session.commit()
    

    return True, f'Reserva de "{exemplar.material.titulo}" para {usuario.nome} realizada com sucesso!'
