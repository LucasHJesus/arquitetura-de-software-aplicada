from sqlalchemy import create_engine, UniqueConstraint, Column, Integer, String, ForeignKey
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="admin",
    host="localhost",
    database="asa_mensageria",
    port=5432
)

engine  = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Curso(Base):
    __tablename__ = 'curso'

    idCurso               = Column(Integer, primary_key=True, autoincrement=True)
    Nome                  = Column(String(45))
    Professor_idProfessor = Column(Integer, ForeignKey('professor.idProfessor'), primary_key=True)
    professor             = relationship('Professor', back_populates='curso')
    curso_aluno           = relationship('CursoAluno', back_populates='curso_')
    __table_args__ = (
        UniqueConstraint('idCurso'),
    )


class Aluno(Base):
    __tablename__ = 'aluno'

    idAluno      = Column(Integer, primary_key=True)
    Nome         = Column(String(45))
    Email        = Column(String(45))
    CPF          = Column(Integer)
    Endereco     = Column(String(45))
    Numero       = Column(Integer)
    Complemento  = Column(String(45))
    Cidade       = Column(String(45))
    Estado       = Column(String(45))
    curso_aluno_ = relationship('CursoAluno', back_populates='aluno_') 

class Professor(Base):
    __tablename__ = 'professor'

    idProfessor  = Column(Integer, primary_key=True)
    Nome         = Column(String(45))
    Email        = Column(String(45))
    CPF          = Column(Integer)
    Endereco     = Column(String(45))
    Numero       = Column(Integer)
    Complemento  = Column(String(45))
    Cidade       = Column(String(45))
    Estado       = Column(String(45))
    curso        = relationship('Curso', back_populates='professor')

class CursoAluno(Base):
    __tablename__ = 'curso_aluno'

    Curso_idCurso = Column(Integer, ForeignKey('curso.idCurso'), primary_key=True)
    Aluno_idAluno = Column(Integer, ForeignKey('aluno.idAluno'), primary_key=True)
    curso_        = relationship('Curso', back_populates='curso_aluno')
    aluno_        = relationship('Aluno', back_populates='curso_aluno_')


Base.metadata.create_all(engine)