import os

def arquivoConf(nome_arquivo):
    
    arquivo_local = nome_arquivo.replace('.toml', '.local.toml')

    if os.path.isfile(arquivo_local):
        return arquivo_local
    else:
        return nome_arquivo

def loadLang(file, lang):
    #internacionalização
    import gettext 
    try:
        localizator = gettext.translation(file, localedir="locales", languages=[lang])
        localizator.install()
        return localizator.gettext
    except:
        return gettext.gettext
    
def secrets():
    import toml

    dados = []

    # Caminho para o arquivo TOM    
    caminho_arquivo_tom = arquivoConf('.streamlit/secrets.toml')

    # Ler o arquivo TOM
    with open(caminho_arquivo_tom, 'r') as arquivo:
        dados = toml.load(arquivo)
    return dados

def conecta():
    from sqlalchemy import create_engine

    confs = secrets()

    # Recuperar os detalhes de conexão do banco de dados
    host = confs['connections']['postgresql']['host']
    database = confs['connections']['postgresql']['database']
    user = confs['connections']['postgresql']['username']
    password = confs['connections']['postgresql']['password']

    return create_engine(f"postgresql://{user}:{password}@{host}:5432/{database}").connect()

def dataFrame(sqlw, columns):
    import pandas as pd
    from sqlalchemy import text
    conn = conecta()

    # Perform query.
    sql_query =  pd.read_sql_query(sql=text(sqlw), con=conn)
    df = pd.DataFrame(sql_query, columns)

    return df

def GET(var, value=""):
    try:
        # Recebe os parâmetros via GET enquanto sem criptografia mandando direto (usar bearertok)
        schemaUsuario = st.query_params.get('usuario', 'SEM_DADOS')
    except:    
        return value

def decodeToken(token, secret_key):
    import jwt
    try:
        return jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.DecodeError as e:
        return e