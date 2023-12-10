from fastapi import FastAPI
from .classes import Request_Professor, Request_Curso, Request_Aluno, Request_CursoAluno
from .models import Professor, Curso, CursoAluno, Aluno, session

app = FastAPI()

# GET ---------------------------------------------------------------
@app.get("/")
async def root():
    return {
        "status": "SUCESS",
        "data": "NO DATAS"
    }

@app.get("/professores")
async def get_all_professores():
    professores_query = session.query(Professor)
    professores = professores_query.all()
    return {
        "status": "SUCESS",
        "data": professores
    }

@app.get("/cursos")
async def get_all_cursos():
    cursos_query = session.query(Curso)
    cursos = cursos_query.all()
    return {
        "status": "SUCESS",
        "data": cursos
    }

@app.get("/curso-aluno")
async def get_all_CursosAlunos():
    CursosAlunos_query = session.query(CursoAluno)
    CursosAlunos = CursosAlunos_query.all()
    return {
        "status": "SUCESS",
        "data": CursosAlunos
    }

@app.get("/alunos")
async def get_all_alunos():
    alunos_query = session.query(Aluno)
    alunos = alunos_query.all()
    return {
        "status": "SUCESS",
        "data": alunos
    }


# PUT ---------------------------------------------------------------
@app.put("/professores")
async def alterar_professor(request_professor: Request_Professor):
    try:    
        professor_json = request_professor
        professor_query = session.query(Professor).filter(
            Professor.idProfessor==professor_json.id
        )
        professor = professor_query.first()
        print(professor.Nome)
        professor.Nome        = professor_json.nome
        professor.Email       = professor_json.email
        professor.CPF         = professor_json.cpf
        professor.Endereco    = professor_json.endereco
        professor.Numero      = professor_json.numero
        professor.Complemento = professor_json.complemento
        professor.Cidade      = professor_json.cidade
        professor.Estado      = professor_json.estado

        session.add(professor_json)
        session.commit()

        return {
            "status": "SUCESS",
            "data": professor_json
        }
    
    except Exception as e:
            return {
                "status": "FAILURE",
                "data": "PROFESSOR NÃO ENCONTRADO"
            }

@app.put("/cursos")
async def alterar_curso(request_curso: Request_Curso):
    try:    
        curso_json = request_curso
        curso_query = session.query(Curso).filter(
            Curso.idCurso==curso_json.id
        )
        curso = curso_query.first()
        print(curso.Nome)
        curso.Nome                  = curso_json.nome
        curso.Professor_idProfessor = curso_json.id_professor

        session.add(curso_json)
        session.commit()

        return {
            "status": "SUCESS",
            "data": curso_json
        }
    
    except Exception as e:
            return {
                "status": "FAILURE",
                "data": "CURSO NÃO ENCONTRADO"
            }

@app.put("/alunos")
async def alterar_aluno(request_aluno: Request_Aluno):
    try:    
        aluno_json = request_aluno
        aluno_query = session.query(Aluno).filter(
            Aluno.idAluno==aluno_json.id
        )
        aluno = aluno_query.first()
        print(aluno.Nome)
        aluno.Nome        = aluno_json.nome
        aluno.Email       = aluno_json.email
        aluno.CPF         = aluno_json.cpf
        aluno.Endereco    = aluno_json.endereco
        aluno.Numero      = aluno_json.numero
        aluno.Complemento = aluno_json.complemento
        aluno.Cidade      = aluno_json.cidade
        aluno.Estado      = aluno_json.estado

        session.add(aluno)
        session.commit()

        return {
            "status": "SUCESS",
            "data": aluno_json
        }
    
    except Exception as e:
            return {
                "status": "FAILURE",
                "data": "ALUNO NÃO ENCONTRADO"
            }

# POST --------------------------------------------------------------
@app.post("/professores")
async def criar_professor(request_professor: Request_Professor):
    professor_json = request_professor
    print(professor_json.nome)

    professor = Professor(
        Nome        = professor_json.nome,
        Email       = professor_json.email,
        CPF         = professor_json.cpf,
        Endereco    = professor_json.endereco,
        Numero      = professor_json.numero,
        Complemento = professor_json.complemento,
        Cidade      = professor_json.cidade,
        Estado      = professor_json.estado
    )
    session.add(professor)
    session.commit()

    return {
        "status": "SUCESS",
        "data": professor_json
    }

@app.post("/cursos")
async def criar_curso(request_curso: Request_Curso):
    curso_json = request_curso
    print(curso_json.nome)

    curso = Curso(
        Nome                  = curso_json.nome,
        Professor_idProfessor = curso_json.id_professor
        
    )
    session.add(curso)
    session.commit()

    return {
        "status": "SUCESS",
        "data": curso_json
    }

@app.post("/alunos")
async def criar_aluno(request_aluno: Request_Aluno):
    aluno_json = request_aluno
    print(aluno_json.nome)

    aluno = Aluno(
        Nome        = aluno_json.nome,
        Email       = aluno_json.email,
        CPF         = aluno_json.cpf,
        Endereco    = aluno_json.endereco,
        Numero      = aluno_json.numero,
        Complemento = aluno_json.complemento,
        Cidade      = aluno_json.cidade,
        Estado      = aluno_json.estado
    )
    session.add(aluno)
    session.commit()

    return {
        "status": "SUCESS",
        "data": aluno_json
    }

@app.post("/curso-aluno")
async def criar_curso_aluno(request_curso_aluno: Request_CursoAluno):
    curso_aluno_json = request_curso_aluno

    curso_aluno = CursoAluno(
        Curso_idCurso       = curso_aluno_json.id_curso,
        Aluno_idAluno       = curso_aluno_json.id_aluno
    )
    session.add(curso_aluno)
    session.commit()

    return {
        "status": "SUCESS",
        "data": curso_aluno_json
    }

# DELETE ------------------------------------------------------------
@app.delete("/professores/")
async def deletar_professor(request_professor: Request_Professor):
    try:
        session.delete(request_professor)
        session.commit()

        return {
            "status": "PROFESSOR EXCLUÍDO!"
        }
    
    except Exception as e:
            return {
                "status": "FAILURE",
                "data": "PROFESSOR NÃO ENCONTRADO"
            }