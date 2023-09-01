from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Aluno(BaseModel):
    nome        :  str
    matricula   :  str
    curso       :  str

@app.get("/")
async def root():
    mensagem = {"response":"suiiii"}
    return mensagem

@app.get("/parametro/{parametro_id}")
async def mostra_parametro(parametro_id):
    mensagem = f"o valor passado foi {parametro_id}"
    return {"response":mensagem}
    
@app.post("/alunos")
async def criar_aluno(aluno:Aluno):
    return aluno