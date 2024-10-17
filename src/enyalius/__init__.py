

def arquivoConf(nome_arquivo, extensao="toml"):
    import os
    
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
    # if connection != False:
    #     return connection
    
    from sqlalchemy import create_engine

    confs = secrets()
    # Recuperar os detalhes de conexão do banco de dados
    host = confs['connections']['postgresql']['host']
    database = confs['connections']['postgresql']['database']
    user = confs['connections']['postgresql']['username']
    password = confs['connections']['postgresql']['password']
    engine = create_engine(f"postgresql://{user}:{password}@{host}:5432/{database}")
    connection = engine.connect()
    return connection, engine

def desconecta(connection, engine):
    connection.close()
    engine.dispose()

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
        import streamlit as st
        # Recebe os parâmetros via GET enquanto sem criptografia mandando direto (usar bearertok)
        return st.query_params.get(var, value)
    except:    
        return value

def decodeToken(token, secret_key):
    import jwt
    try:
        return jwt.decode(token, secret_key, algorithms=["HS256"])
    except jwt.DecodeError as e:
        return e

def decriptaAES(data, secret_key, separator="::"):
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    import base64

    def decode_data(cript):
        
        data_b64 = base64.b64decode(cript)

        eData, iv = data_b64.split(b'::', 1)
        return eData, iv


    def aes_decrypt(ciphertext, key):
        from cryptography.hazmat.primitives import padding
        eData, iv = decode_data(ciphertext)
        ciphertext_bytes = base64.b64decode(eData)

  
        cipher = Cipher(algorithms.AES256(key), mode=modes.CBC(iv))

        decryptor = cipher.decryptor()
        texto_cifrado = decryptor.update(ciphertext_bytes) + decryptor.finalize()
        return texto_cifrado


    import hashlib

    hash_algorithm = hashlib.md5()

    # Atualiza o objeto hash com a chave
    hash_algorithm.update(secret_key.encode())
    # Gera o hash como um objeto bytes
    hashed_key = hash_algorithm.digest()

    # Converte o hash para hexadecimal
    key = hashed_key.hex()

    decrypted_data = aes_decrypt(data, bytes(key, encoding='utf-8'))

    return decrypted_data.decode()

def df_from_disk(file_path):
    """
    Lê um arquivo CSV do disco e retorna um DataFrame do pandas.

    Parameters:
    file_path (str): O caminho do arquivo CSV.

    Returns:
    pandas.DataFrame: DataFrame contendo os dados do arquivo CSV.
    """
    #Eny.ds(file_path)
    import pandas as pd

    df = pd.read_csv(file_path)
    return df

__all__ = ['loadLang', 'secrets', 'dataFrame', 'GET', 'decodeToken', 'df_from_disk']
