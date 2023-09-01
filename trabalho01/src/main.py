""" 
Aluno: Lucas Humberto Jesus de Lima
Matricula:12011ECP011
Arquitetura de software aplicada
Trabalho 01 - CRUD sem banco
 """


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from logging.config import dictConfig
import logging
from .config import log_config

myDict:list = [
    {
        "nome":"Bruno Pavan",
        "matricula":"12011ECP012",
        "curso":"Engenharia de COmputação"
    },
    {
        "nome":"Leonardo Vecchi",
        "matricula":"12011ECP001",
        "curso":"Engenharia de COmputação"
    },
    {
        "nome":"Lucas Jesus",
        "matricula":"12011ECP011",
        "curso":"Engenharia de COmputação"
    }
]

dictConfig(log_config)

app = FastAPI(debug=True)
logger = logging.getLogger('foo-logger')

class Aluno(BaseModel):
    nome: str
    matricula: str
    curso: str
    

@app.get("/")
async def root():
    logger.debug("Aqui na rota principal")
    message = {"response" : "insert /docs into the url to acces Swagger UI"}
    return message

@app.get("/aluno/{matricula}")
async def get_studant_by_id(matricula):
    for item in myDict:
        if item["matricula"] == matricula:
            logger.info(f"GET Request: aluno:{matricula}")
            return {"response" : item}
        
    logger.error(f"GET aluno: Aluno não encontrado: {matricula}")
    raise HTTPException(status_code=404, detail="Aluno nao encontrado!")

@app.get("/aluno")
async def get_studants():

    logger.info("GET Request: Todos os alunos")
    return {"response" : myDict}

@app.post("/alunos")
async def create_studant(aluno : Aluno):

    dict={}
    dict["nome"] = aluno.nome
    dict["matricula"] = aluno.matricula
    dict["curso"] = aluno.curso
    myDict.append(dict)
    logger.info(f"Post Request: Criar aluno:{dict}")

    return aluno

@app.put("/alunos")
async def update_studant(aluno:Aluno):

    message = {}

    for item in myDict:
        if item["matricula"] == aluno.matricula:
            item["nome"] = aluno.nome
            item["curso"] = aluno.curso
            logger.info(f"PUT aluno: aluno atualizado: {aluno.matricula}")
            return {"response":"atualizado"}
        
    logger.error(f"PUT aluno: Aluno não encontrado: {aluno.matricula}")
    raise HTTPException(status_code=404, detail="Aluno nao encontrado!")

@app.delete("/alunos/{matricula}")
async def delete_studant(matricula:str):
    message = {}
    found = False
    for item in myDict:
        if item["matricula"] == matricula:
            message = item
            found = True

    if found:
        myDict.remove(message)

        logger.info("Success")
        return {"response":"Aluno excluido"}
    
    logger.error(f"DELETE aluno: Aluno não encontrado: {matricula}")
    raise HTTPException(status_code=404, detail="Aluno nao encontrado!")