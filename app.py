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


@app.route("/listar_voluntarios", methods=['GET', 'POST'])
def voluntarios():
    if request.method == 'POST':
        dados = request.json
        return jsonify(models.listar_voluntarios(nome=dados['nome_voluntario']))
    else:
        return jsonify(models.listar_voluntarios())


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
