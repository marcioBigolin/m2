import streamlit as st
import pages.Eny.eny as Eny
import Eny.decode as jwt
import base64


st.set_page_config(page_title="Análise por aluno", page_icon="📈")

# Recebe os parâmetros via GET enquanto sem criptografia mandando direto (usar bearertok)
params = st.experimental_get_query_params()
# Obtém o valor do parâmetro 'variavel' da URL
schemaUsuario = params.get('usuario', ['SEM_DADOS'])[0]  
aluno = params.get('aluno', ['SEM_DADOS'])[0]  
encode = params.get('encode', ['SEM_DADOS'])[0]  

confs = Eny.secrets()['geral']

decode = jwt.decodeToken(encode, confs['jwt'])

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def decode_data(cript):
    
    data_b64 = base64.b64decode(cript)
    st.text(data_b64)

    eData, iv = data_b64.split(b'::', 1)
    return eData, iv


def aes_decrypt(ciphertext, key):
    from cryptography.hazmat.primitives import padding
    st.text(ciphertext)
    eData, iv = decode_data(ciphertext)
    ciphertext_bytes = base64.b64decode(eData)

    st.text(iv)
    st.text(ciphertext_bytes)

    cipher = Cipher(algorithms.AES256(key), mode=modes.CBC(iv))

    decryptor = cipher.decryptor()
    texto_cifrado = decryptor.update(ciphertext_bytes) + decryptor.finalize()
    return texto_cifrado


import hashlib

hash_algorithm = hashlib.md5()

# Atualiza o objeto hash com a chave
hash_algorithm.update(confs['jwt'].encode())
# Gera o hash como um objeto bytes
hashed_key = hash_algorithm.digest()

# Converte o hash para hexadecimal
key = hashed_key.hex()

st.text(key)
st.text(bytes(key, encoding='utf-8'))


st.text(decode)

decrypted_data = aes_decrypt(decode['data']['schema'], bytes(key, encoding='utf-8'))

st.text(decrypted_data.decode())  # Saída: "dado_confidencial"

