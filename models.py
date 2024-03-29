import datetime
import os
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


def get_colunas_tabela(nome_tabela, cursor, indentificacao: bool = False) -> list:
    cursor.execute(f"PRAGMA table_info({nome_tabela});")
    resultados = cursor.fetchall()

    if indentificacao:
        return [f'{resultado[1]}_{nome_tabela}' for resultado in resultados]
    else:
        return [resultado[1] for resultado in resultados]


def get_placeholders(colunas: list, usa_colunas: bool) -> str:
    if usa_colunas:
        return ', '.join(colunas)
    return ', '.join(['?' for _ in range(len(colunas))])


def preparar_query_generica(nome_tabela: str, lista_filtros: list) -> str:
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


def alterar_registro_tabela(nome_tabela: str, dados: dict, key: str = 'codigo'):
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
            WHERE codigo = {dados[key]};
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

    query = preparar_query_generica(nome_tabela, lista_filtros)
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


def apagar_foto_antiga(cod_aluno: int):
    arquivo = get_foto_aluno(cod_aluno)
    os.remove(os.path.join("imagens", arquivo))


def atualizar_aluno(dados: dict):
    oficinas = [key for key in list(dados.keys()) if 'oficina' in key]
    for ofc in oficinas:
        del dados[ofc]

    chave_foto = list(dados.keys())[1]
    dados[chave_foto] = imagemB64.base64_to_image(dados[chave_foto])
    dados['dt_alteracao'] = datetime.date.today().strftime("%Y-%m-%d")

    apagar_foto_antiga(dados['codigo'])
    alterar_registro_tabela('aluno', dados)


def get_aluno(codigo: int) -> dict:
    nome_tabela = 'aluno'
    conexao, cursor = abrir_conexao()
    cursor.execute(f"""
        SELECT *
        FROM {nome_tabela}
            INNER JOIN responsavel AS R ON R.codigo = cod_responsavel 
        WHERE {nome_tabela}.codigo = {codigo}
    """)
    resultado = cursor.fetchone()

    if resultado:
        colunas = get_colunas_tabela(nome_tabela, cursor) + \
                  get_colunas_tabela('responsavel', cursor, True)
        dicionario = criar_dicionario(colunas, resultado)
        fechar_conexao(conexao, False)

        dicionario['foto'] = imagemB64.image_to_base64(dicionario['foto'])
        return dicionario
    else:
        return {}


def get_foto_aluno(codigo: int):
    nome_tabela = 'aluno'
    conexao, cursor = abrir_conexao()
    cursor.execute(f"SELECT foto FROM {nome_tabela} WHERE codigo = {codigo}")
    foto = str(cursor.fetchone()[0])
    fechar_conexao(conexao, False)
    return foto


def get_alunos_mesmo_responsavel(cod_aluno, cod_responsavel) -> list:
    nome_tabela = 'aluno'
    conexao, cursor = abrir_conexao()
    cursor.execute(f"""
            SELECT codigo, nome
            FROM {nome_tabela}
            WHERE cod_responsavel = {cod_responsavel}
                AND codigo <> {cod_aluno}
            ORDER BY nome
        """)
    resultado = cursor.fetchall()

    colunas = ['codigo', 'nome']
    alunos = [criar_dicionario(colunas, res) for res in resultado]
    fechar_conexao(conexao, False)
    return alunos


def listar_alunos(nome: str = '', sexo: str = '', idades: dict = None) -> list:
    lista_filtros = []
    nome_tabela = 'aluno'
    conexao, cursor = abrir_conexao()

    lista_filtros.append(f"nome LIKE '%{nome}%'" if nome else '')
    lista_filtros.append(f"sexo = '{sexo}'" if sexo else '')

    if idades:
        idade_inicial = idades['idade1']
        idade_final = idades['idade2']

        if idade_inicial and not idade_final:
            lista_filtros.append(f'idade = {idade_inicial}')
        elif (idade_inicial and idade_final) or (not idade_inicial and idade_final):
            lista_filtros.append(f'idade BETWEEN {idade_inicial} AND {idade_final}')

    query = preparar_query_generica(nome_tabela, lista_filtros)
    cursor.execute(query)
    resultado = cursor.fetchall()

    if resultado:
        lista_alunos = list()
        for res in resultado:
            lista_alunos.append(criar_dicionario(get_colunas_tabela(nome_tabela, cursor), res))

        fechar_conexao(conexao, False)
        return lista_alunos
    else:
        return []


def set_responsavel(dados: dict):
    return inserir_registro_tabela('responsavel', dados)


def atualizar_responsavel(dados: dict):
    alterar_registro_tabela('responsavel', dados, 'codigo_responsavel')


def listar_escolas():
    nome_tabela = 'escola'
    conexao, cursor = abrir_conexao()
    cursor.execute(f"SELECT * FROM {nome_tabela} ORDER BY nome")
    resultado = cursor.fetchall()
    colunas = get_colunas_tabela(nome_tabela, cursor)
    lista_escolas = [criar_dicionario(colunas, valores) for valores in resultado]

    fechar_conexao(conexao, False)
    return lista_escolas


