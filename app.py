import time

from flask import Flask, request, jsonify, session
from flask_cors import CORS	   # pip install -U flask-cors

import models

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

app.secret_key = 'dflkdlh98343hindq123093nryoqywyo37t6dfowqynfo7ev8de78ydubogs'


@app.route("/logar_usuario", methods=['POST'])
def login():
    if request.method == 'POST':
        dados = request.json
        usuario = dados['usuario']
        senha = dados['senha']

        for usuario_bd in models.listar_voluntarios():
            if usuario == usuario_bd['usuario'] and senha == usuario_bd['senha']:
                session['usuario'] = usuario_bd['codigo']
                session['tipo_acesso'] = usuario_bd['tipo_acesso']

                return jsonify({
                    'status': 'success',
                    'codigo': usuario_bd['codigo'],
                    'tipo_acesso': usuario_bd['tipo_acesso']
                })

        return jsonify({
            'status': 'danger',
            'mensagem': 'Usuário ou senha incorretos'
        })


@app.route("/listar_escolas", methods=['GET'])
def escolas():
    if request.method == 'GET':
        return jsonify(models.listar_escolas())


@app.route("/registrar_aluno", methods=['POST'])
def addAluno():
    if request.method == 'POST':
        dados = request.json

        cod_reponsavel = models.set_responsavel(dados['responsavel'])
        del dados['responsavel']

        for aluno, atributos in dados.items():
            models.set_aluno(atributos, cod_reponsavel)

        return jsonify({'status': 'success'})


@app.route("/listar_voluntarios", methods=['GET', 'POST'])
def voluntarios():
    if request.method == 'POST':
        dados = request.json
        return jsonify(models.listar_voluntarios(nome=dados['nome_voluntario']))
    else:
        return jsonify(models.listar_voluntarios())


@app.route("/listar_alunos", methods=['GET', 'POST'])
def alunos():
    if request.method == 'POST':
        dados = request.json
        alunos = models.listar_alunos(
            nome=dados['nome'],
            sexo=dados['sexo'],
            idades={
                'idade1': int(dados['idade1']) if dados['idade1'] else 0,
                'idade2': int(dados['idade2']) if dados['idade2'] else 0
            }
        )
    else:
        alunos = models.listar_alunos()

    return jsonify({
        'alunos': alunos,
        'quantidade': len(alunos)
    })


@app.route("/visualizar_aluno", methods=['GET'])
def visualizar_aluno(codigo: int):
    if request.method == 'GET':
        aluno = models.get_aluno(codigo)

        if aluno:
            alunos_mesmo_responsavel = models.get_alunos_mesmo_responsavel(aluno['codigo'], aluno['cod_responsavel'])

            return jsonify({
                'aluno': aluno,
                'outros_alunos': alunos_mesmo_responsavel,
                'success': 'Aluno encontrado!'
            })

        return jsonify({
            'danger': 'Aluno não encontrado!',
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)




















