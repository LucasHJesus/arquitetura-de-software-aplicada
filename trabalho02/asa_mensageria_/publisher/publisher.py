# BACKEND :)

from fastapi import FastAPI
from .classes import Request_Professor, Request_Curso, Request_Aluno, Request_CursoAluno
import json
import pika


app = FastAPI()

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost',
                                   5672,
                                   '/',
                                   credentials)

# POST --------------------------------------------------------------
@app.post("/professores")
async def criar_professor(request_professor: Request_Professor):
    professor_json = {
        "id"         : request_professor.id,
        "nome"       : request_professor.nome,
        "email"      : request_professor.email,
        "cpf"        : request_professor.cpf,
        "endereco"   : request_professor.endereco,
        "numero"     : request_professor.numero,
        "complemento": request_professor.complemento,
        "cidade"     : request_professor.cidade,
        "estado"     : request_professor.estado
    }
    queuename = 'professorinsert'
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queuename)
    channel.basic_publish(exchange='', routing_key=queuename, body=json.dumps(professor_json))
    channel.close()

    return {
            "status": "SUCESS",
            "data": professor_json
        }

@app.post("/cursos")
async def criar_curso(request_curso: Request_Curso):
    curso_json = {
        "id"          : request_curso.id,
        "nome"        : request_curso.nome,
        "id_professor": request_curso.id_professor
    }
    queuename = 'cursoinsert'
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queuename)
    channel.basic_publish(exchange='', routing_key=queuename, body=json.dumps(curso_json))
    channel.close()
    return {
            "status": "SUCESS",
            "data": curso_json
        }

@app.post("/alunos")
async def criar_aluno(request_aluno: Request_Aluno):
    aluno_json = {
        "id"         : request_aluno.id,
        "nome"       : request_aluno.nome,
        "email"      : request_aluno.email,
        "cpf"        : request_aluno.cpf,
        "endereco"   : request_aluno.endereco,
        "numero"     : request_aluno.numero,
        "complemento": request_aluno.complemento,
        "cidade"     : request_aluno.cidade,
        "estado"     : request_aluno.estado
    }
    queuename = 'alunoinsert'
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queuename)
    channel.basic_publish(exchange='', routing_key=queuename, body=json.dumps(aluno_json))
    channel.close()

    return {
            "status": "SUCESS",
            "data": aluno_json
        }

@app.post("/curso-aluno")
async def criar_curso_aluno(request_curso_aluno: Request_CursoAluno):
    curso_aluno_json = {
        "id_curso": request_curso_aluno.id_curso,
        "id_aluno": request_curso_aluno.id_aluno
    }
    queuename = 'cursoalunoinsert'
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=queuename)
    channel.basic_publish(exchange='', routing_key=queuename, body=json.dumps(curso_aluno_json))
    channel.close()

    return {
            "status": "SUCESS",
            "data": curso_aluno_json
        }