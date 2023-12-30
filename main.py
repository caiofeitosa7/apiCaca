from fastapi import FastAPI
import models

app = FastAPI()


@app.get("/")
async def root():
    return 'Ola mundo'


@app.post("/login")
def login(json):
    usuario = json['usuario']
    senha = json['senha']

    print(usuario, senha)

    dados = models.get_usuario(usuario)

    if not dados:
        return {
            'erro': 'Usuario nao encontrado'
        }
    
    if usuario == dados['usuario'] and senha == dados['senha']:
        return {
            'codigo': dados['codigo'],
            'nome': dados['nome'],
            'funcao': dados['funcao'],
            'tipo_acesso': dados['senha']
        }
    else:
        return {
            'erro': 'Usuario ou senha incorretos'
        }


@app.get("/login")
def login(usuario, senha):
    dados = models.get_usuario(usuario)

    if not dados:
        return {
            'erro': 'Usuario nao encontrado'
        }
    
    if usuario == dados['usuario'] and senha == dados['senha']:
        return {
            'codigo': dados['codigo'],
            'nome': dados['nome'],
            'funcao': dados['funcao'],
            'tipo_acesso': dados['tipo_acesso']
        }
    else:
        return {
            'erro': 'Usuario ou senha incorretos'
        }