from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import date, timedelta

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome = Column(String(255))
    matricula = Column(String(50), unique=True)
    tipo = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'usuario',
        'polymorphic_on': tipo
    }

    emprestimos = relationship('Emprestimo', back_populates='usuario')

class Aluno(Usuario):
    __tablename__ = 'alunos'
    id = Column(Integer, ForeignKey('usuarios.id'), primary_key=True)
    curso = Column(String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'aluno',
    }

class Professor(Usuario):
    __tablename__ = 'professores'
    id = Column(Integer, ForeignKey('usuarios.id'), primary_key=True)
    departamento = Column(String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'professor',
    }

class Funcionario(Usuario):
    __tablename__ = 'funcionarios'
    id = Column(Integer, ForeignKey('usuarios.id'), primary_key=True)
    setor = Column(String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'funcionario',
    }

class Autor(Base):
    __tablename__ = 'autores'
    id = Column(Integer, primary_key=True)
    nome = Column(String(255))

    obras = relationship('Material', secondary='material_autor', back_populates='autores')

class Material(Base):
    __tablename__ = 'materiais'
    id = Column(Integer, primary_key=True)
    titulo = Column(String(255))
    ano_publicacao = Column(Integer)
    tipo = Column(String(50))
    
    __mapper_args__ = {
        'polymorphic_identity': 'material',
        'polymorphic_on': tipo
    }
    
    exemplares = relationship('Exemplar', back_populates='material')
    autores = relationship('Autor', secondary='material_autor', back_populates='obras')

class Livro(Material):
    __tablename__ = 'livros'
    id = Column(Integer, ForeignKey('materiais.id'), primary_key=True)
    edicao = Column(String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'livro',
    }

class Dissertacao(Material):
    __tablename__ = 'dissertacoes'
    id = Column(Integer, ForeignKey('materiais.id'), primary_key=True)
    programa_pos = Column(String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'dissertacao',
    }

class Tese(Material):
    __tablename__ = 'teses'
    id = Column(Integer, ForeignKey('materiais.id'), primary_key=True)
    programa_pos = Column(String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'tese',
    }
    
class MaterialAutor(Base):
    __tablename__ = 'material_autor'
    autor_id = Column(Integer, ForeignKey('autores.id'), primary_key=True)
    material_id = Column(Integer, ForeignKey('materiais.id'), primary_key=True)

class Exemplar(Base): # versao física do material (livro, tese ou dissertação)
    __tablename__ = 'exemplares'
    id = Column(Integer, primary_key=True)
    disponivel = Column(Integer)
    material_id = Column(Integer, ForeignKey('materiais.id'))

    material = relationship('Material', back_populates='exemplares')
    emprestimos = relationship('Emprestimo', back_populates='exemplar')
    reservas = relationship('Reserva', back_populates='exemplar')

class Emprestimo(Base):
    __tablename__ = 'emprestimos'
    id = Column(Integer, primary_key=True)
    data_emprestimo = Column(Date)
    data_devolucao = Column(Date, nullable=True)
    multa = Column(Integer, default=0)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    exemplar_id = Column(Integer, ForeignKey('exemplares.id'))
    
    usuario = relationship('Usuario', back_populates='emprestimos')
    exemplar = relationship('Exemplar', back_populates='emprestimos')

    def calcular_multa(self):
        if self.data_devolucao is not None:
            return  

        prazo_devolucao = timedelta(days=7)
        data_vencimento = self.data_emprestimo + prazo_devolucao

        # Se ainda não devolveu, calcula multa em tempo real
        data_referencia = date.today()

        if data_referencia > data_vencimento:
            dias_atraso = (data_referencia - data_vencimento).days
            self.multa = dias_atraso * 1.0  # R$ 1 por dia de atraso
        else:
            self.multa = 0.0

class Reserva(Base):
    __tablename__ = 'reservas'
    id = Column(Integer, primary_key=True)
    data_reserva = Column(Date)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    exemplar_id = Column(Integer, ForeignKey('exemplares.id'))
    
    usuario = relationship('Usuario')
    exemplar = relationship('Exemplar', back_populates='reservas')