from pydantic import BaseModel


class Request_Professor(BaseModel):
    id:          int
    nome:        str
    email:       str
    cpf:         str
    endereco:    str
    numero:      int
    complemento: str
    cidade:      str
    estado:      str


class Request_Curso(BaseModel):
    id:           int
    nome:         str
    id_professor: int


class Request_Aluno(BaseModel):
    id:          int
    nome:        str
    email:       str
    cpf:         int
    endereco:    str
    numero:      int
    complemento: str
    cidade:      str
    estado:      str

class Request_CursoAluno(BaseModel):
    id_curso: int
    id_aluno: int