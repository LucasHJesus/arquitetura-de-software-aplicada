from fastapi import FastAPI
from .classes import Request_Aluno
from .models import Aluno, session
app = FastAPI()




@app.get("/")
async def root():
    return {
        "status": "SUCESS",
        "data": "NO DATAS"
    }

@app.get("/alunos")
async def get_all_alunos():
    alunos_query = session.query(Aluno)
    alunos = alunos_query.all()
    return {
        "status": "SUCESS",
        "data": alunos
    }

@app.put("/alunos")
async def alterar_aluno(request_aluno: Request_Aluno):
    try:    
        aluno_json = request_aluno
        aluno_query = session.query(Aluno).filter(
            Aluno.id==aluno_json.id
        )
        aluno = aluno_query.first()
        if aluno == None:
             return {
                "status": "SUCESS",
                "data": "ALUNO NÃO ENCONTRADO"
            }
        print(aluno.nome)
        aluno.nome = aluno_json.nome
        aluno.cpf = aluno_json.cpf
        aluno.email = aluno_json.email
        aluno.endereco = aluno_json.endereco

        session.add(aluno)
        session.commit()

        return {
            "status": "SUCESS",
            "data": aluno_json
        }
    
    except Exception as e:
            return {
                "status": "SUCESS",
                "data": "ALUNO NÃO ENCONTRADO"
            }


@app.post("/alunos")
async def criar_aluno(request_aluno: Request_Aluno):
    aluno_json = request_aluno
    print(aluno_json.nome)

    aluno = Aluno(
        nome     = aluno_json.nome,
        email    = aluno_json.endereco,
        cpf      = aluno_json.cpf,
        endereco = aluno_json.endereco
    )
    session.add(aluno)
    session.commit()

    return {
        "status": "SUCESS",
        "data": aluno_json
    }


from .classes import Request_Professor
from .models import Professor, session

@app.get("/professores")
async def get_all_professores():
    professores_query = session.query(Professor)
    professores = professores_query.all()
    return {
        "status": "SUCESS",
        "data": professores
    }

@app.put("/professores")
async def alterar_professor(request_professor: Request_Professor):
    try:    
        professor_json = request_professor
        professor_query = session.query(Professor).filter(
            Professor.id==professor_json.id
        )
        professor = professor_query.first()
        if professor == None:
             return {
                "status": "SUCESS",
                "data": "ALUNO NÃO ENCONTRADO"
            }
        print(professor.nome)
        professor.nome = professor_json.nome
        professor.cpf = professor_json.cpf
        professor.email = professor_json.email
        professor.endereco = professor_json.endereco

        session.add(professor)
        session.commit()

        return {
            "status": "SUCESS",
            "data": professor_json
        }
    
    except Exception as e:
            return {
                "status": "SUCESS",
                "data": "ALUNO NÃO ENCONTRADO"
            }


@app.post("/professores")
async def criar_professor(request_professor: Request_Professor):
    professor_json = request_professor
    print(professor_json.nome)

    professor = Professor(
        nome     = professor_json.nome,
        email    = professor_json.endereco,
        cpf      = professor_json.cpf,
        endereco = professor_json.endereco
    )
    session.add(professor)
    session.commit()

    return {
        "status": "SUCESS",
        "data": professor_json
    }