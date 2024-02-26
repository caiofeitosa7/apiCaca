import datetime
import sqlite3
import imagemB64


def abrir_conexao():
    conexao = sqlite3.connect("caca.db3")
    cursor = conexao.cursor()
    return conexao, cursor


def fechar_conexao(conexao, commit: bool = True):
    if commit:
        conexao.commit()
    conexao.close()


def criar_dicionario(colunas: list, valores: tuple) -> dict:
    dados = dict()
    for i, coluna in enumerate(colunas):
        dados[coluna] = valores[i]

    return dados


def get_colunas_tabela(nome_tabela: str, cursor) -> list:
    cursor.execute(f"PRAGMA table_info({nome_tabela});")
    resultados = cursor.fetchall()
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


def inserir_registro_tabela(nome_tabela: str, dados: dict):
    conexao, cursor = abrir_conexao()
    valores = tuple(dados.values())
    colunas = get_colunas_tabela(nome_tabela, cursor)

    query = f"""INSERT INTO {nome_tabela} (
                    {get_placeholders(colunas[1:], True)}
                ) VALUES (
                    {get_placeholders(colunas[1:], False)}
                )
            """

    try:
        cursor = conexao.cursor()
        cursor.execute(query, valores)
        cod_registro = cursor.lastrowid
        fechar_conexao(conexao)

        return cod_registro
    except Exception as e:
        print(e)


def alterar_registro_tabela(nome_tabela: str, dados: dict):
    conexao, cursor = abrir_conexao()
    valores = tuple(dados.values())[1:]
    colunas = get_colunas_tabela(nome_tabela, cursor)

    lista = list()
    for i, coluna in enumerate(colunas[1:]):
        lista.append(f"{coluna} = ?")

    query = f"""
            UPDATE {nome_tabela}
            SET 
                {get_placeholders(lista, True)}
            WHERE codigo = {dados['codigo']};
        """

    try:
        cursor.execute(query, valores)
        fechar_conexao(conexao)
    except Exception as e:
        print(e)


def apagar_registro_tabela(nome_tabela: str, codigo: int):
    conexao, cursor = abrir_conexao()
    query = f"DELETE FROM {nome_tabela} WHERE codigo = {codigo}"
    cursor.execute(query)
    fechar_conexao(conexao)


def listagem_basica(nome_tabela) -> list:
    conexao, cursor = abrir_conexao()
    query = f"SELECT * FROM {nome_tabela}"
    cursor.execute(query)
    resultados = cursor.fetchall()
    colunas = get_colunas_tabela(nome_tabela, cursor)

    fechar_conexao(conexao)
    return [criar_dicionario(colunas, list(resultado)) for resultado in resultados]


def set_voluntario(dados: dict):
    conexao, cursor = abrir_conexao()
    valores = tuple(dados.values())
    nome_tabela = 'voluntario'

    colunas = get_colunas_tabela(nome_tabela, cursor)
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

    if resultado:
        dicionario = criar_dicionario(get_colunas_tabela(nome_tabela, cursor), resultado)
        fechar_conexao(conexao, False)
        return dicionario
    else:
        return {}


def listar_voluntarios(codigo: int = 0, nome: str = '') -> list:
    lista_filtros = []
    nome_tabela = 'voluntario'
    conexao, cursor = abrir_conexao()

    lista_filtros.append(f'codigo = {codigo}' if codigo else '')
    lista_filtros.append(f"nome LIKE '%{nome}%'" if nome else '')

    query = preparar_query(nome_tabela, lista_filtros)
    cursor.execute(query)
    resultado = cursor.fetchall()

    if resultado:
        lista_voluntarios = list()
        for res in resultado:
            lista_voluntarios.append(criar_dicionario(get_colunas_tabela(nome_tabela, cursor), res))

        fechar_conexao(conexao, False)
        return lista_voluntarios
    else:
        return []


def set_aluno(dados: dict, cod_responsavel: int):
    chave_foto = list(dados.keys())[0]
    dados[chave_foto] = imagemB64.base64_to_image(dados[chave_foto])
    dados['dt_alteracao'] = datetime.date.today().strftime("%Y-%m-%d")
    dados['cod_responsavel'] = cod_responsavel

    oficinas = [key for key in list(dados.keys()) if 'oficina' in key]
    for ofc in oficinas:
        del dados[ofc]

    inserir_registro_tabela('aluno', dados)


def get_aluno(codigo: int) -> dict:
    nome_tabela = 'aluno'
    conexao, cursor = abrir_conexao()
    cursor.execute(f"SELECT * FROM {nome_tabela} WHERE codigo = {codigo}")
    resultado = cursor.fetchone()

    if resultado:
        dicionario = criar_dicionario(get_colunas_tabela(nome_tabela, cursor), resultado)
        fechar_conexao(conexao, False)
        return dicionario
    else:
        return {}
    

def listar_alunos(cpf: int = 0, nome: str = '', escola: str = '', idades: dict = None) -> list:
    lista_filtros = []
    nome_tabela = 'aluno'
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

    if resultado:
        lista_voluntarios = list()
        for res in resultado:
            lista_voluntarios.append(criar_dicionario(get_colunas_tabela(nome_tabela, cursor), res))

        fechar_conexao(conexao, False)
        return lista_voluntarios
    else:
        return []


def listar_escolas():
    nome_tabela = 'escola'
    conexao, cursor = abrir_conexao()
    cursor.execute(f"SELECT * FROM {nome_tabela} ORDER BY nome")
    resultado = cursor.fetchall()
    colunas = get_colunas_tabela(nome_tabela, cursor)
    lista_escolas = [criar_dicionario(colunas, valores) for valores in resultado]

    fechar_conexao(conexao, False)
    return lista_escolas


def set_responsavel(dados: dict):
    print(dados)
    return inserir_registro_tabela('responsavel', dados)





# set_responsavel({
#     'nome_responsavel': 'oi',
#     'cpf_responsavel': 'caio',
#     'endereco_responsavel': 'rua',
#     'fone_responsavel': '95',
#     'ocupacao_responsavel': 'prog'
# })



# print(listar_voluntarios(nome='caio'))
# print(listar_alunos(idades={'idade1': 10, 'idade2': 30}))
# print(listar_alunos(nome='ana'))

