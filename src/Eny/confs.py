def arquivoConf(nome_arquivo):
    import os
    arquivo_local = nome_arquivo.replace('.toml', '.local.toml')

    if os.path.isfile(arquivo_local):
        return arquivo_local
    else:
        return nome_arquivo

def secrets():
    import toml

    dados = []

    # Caminho para o arquivo TOM    
    caminho_arquivo_tom = arquivoConf('.streamlit/secrets.toml')


    # Ler o arquivo TOM
    with open(caminho_arquivo_tom, 'r') as arquivo:
        dados = toml.load(arquivo)
    return dados