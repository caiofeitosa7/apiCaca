from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Precisa liberar acesso à todas as origens quando Front e Back rodam no localhost (CORS)
import models

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return 'Ola mundo'


@app.post("/logar_usuario")
def login(dados: dict):
    usuario = str(dados['usuario'])
    senha = str(dados['senha'])

    for usuario_bd in models.listar_voluntarios():
        if usuario == usuario_bd['usuario'] and senha == usuario_bd['senha']:
            return {
                'status': 'success',
                'codigo': usuario_bd['codigo'],
                'nome': usuario_bd['nome'],
                'funcao': usuario_bd['funcao'],
                'disponivel': usuario_bd['disponivel'],
                'tipo_acesso': usuario_bd['senha']
            }
    
    return {
        'status': 'danger',
        'messagem': 'Usuario ou senha incorretos'
    }


@app.get("/login")
def login(usuario, senha):
    dados = models.get_voluntario(usuario)

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
