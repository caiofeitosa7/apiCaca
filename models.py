import sqlite3


def criar_dicionario(colunas: list, valores: tuple) -> dict:
    dados = dict()
    for i, coluna in enumerate(colunas):
        dados[coluna] = valores[i]

    return dados


def get_colunas_tabela(nome_tabela: str) -> list:
    conexao, cursor = abrir_conexao()
    cursor.execute(f"PRAGMA table_info({nome_tabela});")
    resultados = cursor.fetchall()
    fechar_conexao(conexao)

    return [resultado[1] for resultado in resultados]


def get_placeholders(colunas: list, usa_colunas: bool) -> str:
    if usa_colunas:
        return ', '.join(colunas)
    return ', '.join(['?' for _ in range(len(colunas))])


def preparar_query(nome_tabela: str, lista_filtros: list) -> str:
    clausura_where = ''
    for filtro in lista_filtros:
        if filtro:
            if clausura_where:
                clausura_where += " AND "
            clausura_where += filtro

    query = f"SELECT * FROM {nome_tabela}"
    query += f" WHERE {clausura_where}" if clausura_where else ""

    return query


def abrir_conexao():
    conexao = sqlite3.connect("caca.db3")
    cursor = conexao.cursor()
    return conexao, cursor


def fechar_conexao(conexao, commit: bool = True):
    if commit:
        conexao.commit()
    conexao.close()


def set_voluntaio(dados: dict):
    nome_tabela = 'voluntario'
    colunas = get_colunas_tabela(nome_tabela)
    conexao, cursor = abrir_conexao()
    valores = tuple(dados.values())
    query = f"""INSERT INTO {nome_tabela} (
            {get_placeholders(colunas[1:], True)}
        ) VALUES (
            {get_placeholders(colunas[1:], False)}
        )
    """

    cursor.execute(query, valores)
    fechar_conexao(conexao)


def get_voluntario(usuario: str) -> dict:
    nome_tabela = 'voluntario'
    conexao, cursor = abrir_conexao()
    cursor.execute(f"SELECT * FROM {nome_tabela} WHERE usuario = '{usuario}'")
    resultado = cursor.fetchone()
    fechar_conexao(conexao, False)

    if resultado:
        return criar_dicionario(get_colunas_tabela(nome_tabela), resultado)
    else:
        return {}


def listar_voluntarios(codigo: int = 0, nome: str = '') -> list:
    lista_filtros = []
    nome_tabela = 'voluntario'
    conexao, cursor = abrir_conexao()

    lista_filtros.append(f'codigo = {codigo}' if codigo else '')
    lista_filtros.append(f'nome = {nome}' if nome else '')

    query = preparar_query(nome_tabela, lista_filtros)
    cursor.execute(query)
    resultado = cursor.fetchall()
    fechar_conexao(conexao, False)

    if resultado:
        lista_voluntarios = list()
        for res in resultado:
            lista_voluntarios.append(criar_dicionario(get_colunas_tabela(nome_tabela), res))

        return lista_voluntarios
    else:
        return []
    

def set_crianca(dados: dict):
    nome_tabela = 'crianca'
    colunas = get_colunas_tabela(nome_tabela)
    conexao, cursor = abrir_conexao()
    valores = tuple(dados.values())
    query = f"""INSERT INTO {nome_tabela} (
            {get_placeholders(colunas[1:], True)}
        ) VALUES (
            {get_placeholders(colunas[1:], False)}
        )
    """

    cursor.execute(query, valores)
    fechar_conexao(conexao)


def get_crianca(codigo: int) -> dict:
    nome_tabela = 'crianca'
    conexao, cursor = abrir_conexao()
    cursor.execute(f"SELECT * FROM {nome_tabela} WHERE codigo = {codigo}")
    resultado = cursor.fetchone()
    fechar_conexao(conexao, False)

    if resultado:
        return criar_dicionario(get_colunas_tabela(nome_tabela), resultado)
    else:
        return {}
    

def listar_criancas(cpf: int = 0, nome: str = '', escola: str = '', idades: dict = None) -> list:
    lista_filtros = []
    nome_tabela = 'crianca'
    conexao, cursor = abrir_conexao()

    lista_filtros.append(f'cpf = {cpf}' if cpf else '')
    lista_filtros.append(f"nome LIKE '%{nome}%'" if nome else '')
    lista_filtros.append(f"escola = '{escola}'" if escola else '')

    if idades:
        idade_inicial = idades['idade1']
        idade_final = idades['idade2']

        if idade_inicial and not idade_final:
            lista_filtros.append(f'idade = {idade_inicial}')
        else:
            lista_filtros.append(f'idade BETWEEN {idade_inicial} AND {idade_final}')

    query = preparar_query(nome_tabela, lista_filtros)
    cursor.execute(query)
    resultado = cursor.fetchall()
    fechar_conexao(conexao, False)

    if resultado:
        lista_voluntarios = list()
        for res in resultado:
            lista_voluntarios.append(criar_dicionario(get_colunas_tabela(nome_tabela), res))

        return lista_voluntarios
    else:
        return []
