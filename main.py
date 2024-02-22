import models
from fastapi import FastAPI

# Precisa liberar acesso à todas as origens quando Front e Back rodam no localhost (CORS)
from fastapi.middleware.cors import CORSMiddleware

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
                'tipo_acesso': usuario_bd['tipo_acesso']
            }

    return {
        'status': 'danger',
        'mensagem': 'Usuário ou senha incorretos'
    }


@app.post("/listar_voluntario")
def listar_voluntarios():
    dados = models.listar_voluntarios(usuario)

