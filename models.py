import sqlite3


def criar_dicionario(colunas, valores):
    dados = dict()
    for i, coluna in enumerate(colunas):
        dados[coluna] = valores[i]

    return dados


def get_colunas_tabela(nome_tabela: str):
    conexao, cursor = abrir_conexao()
    cursor.execute(f"PRAGMA table_info({nome_tabela});")
    resultados = cursor.fetchall()
    fechar_conexao(conexao)

    return [resultado[1] for resultado in resultados]


def get_placeholders(colunas):
    return ', '.join(['?' for _ in range(len(colunas))])


def abrir_conexao():
    conexao = sqlite3.connect("caca.db3")
    cursor = conexao.cursor()

    return conexao, cursor


def fechar_conexao(conexao, commit: bool = True):
    if commit:
        conexao.commit()
    conexao.close()


def get_usuario(usuario: str):
    nome_tabela = 'voluntario'
    conexao, cursor = abrir_conexao()
    cursor.execute(f"SELECT * FROM {nome_tabela} WHERE usuario = '{usuario}'")
    resultado = cursor.fetchone()
    fechar_conexao(conexao, False)

    if resultado:
        return criar_dicionario(get_colunas_tabela(nome_tabela), resultado)
    else:
        return {}


def set_crianca(dados: dict):
    nome_tabela = 'crianca'
    colunas = get_colunas_tabela(nome_tabela)
    conexao, cursor = abrir_conexao()
    valores = tuple(dados.values())
    query = f"""INSERT INTO {nome_tabela} (
            {colunas[1]},
            {colunas[2]},
            {colunas[3]},
            {colunas[4]},
            {colunas[5]},
            {colunas[6]},
            {colunas[7]},
            {colunas[8]},
            {colunas[9]},
            {colunas[10]}
        ) VALUES ({get_placeholders(colunas[1:])})
    """

    cursor.execute(query, valores)
    fechar_conexao(conexao)


def get_crianca(codigo: int):
    nome_tabela = 'crianca'
    conexao, cursor = abrir_conexao()
    cursor.execute(f"SELECT * FROM {nome_tabela} WHERE codigo = {codigo}")
    resultado = cursor.fetchone()
    fechar_conexao(conexao, False)

    if resultado:
        return criar_dicionario(get_colunas_tabela(nome_tabela), resultado)
    else:
        return {}
    

# print(get_usuario('caio'))
print(get_crianca(1))
# print(get_colunas_tabela('crianca'))

colunas = get_colunas_tabela('crianca')

# set_crianca({
#     colunas[1]: 'ana',
#     colunas[2]: 444,
#     colunas[3]: 555,
#     colunas[4]: 'rua 2, casa 10',
#     colunas[5]: 'francisco prado',
#     colunas[6]: '5 ano do ensino fundamental',
#     colunas[7]: '12345678',
#     colunas[8]: '',
#     colunas[9]: 12,
#     colunas[10]: '2002-23-03'
# })