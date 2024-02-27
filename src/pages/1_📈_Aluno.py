import streamlit as st
import Eny.confs as Eny
import Eny.decode as jwt
import pandas as pd
from locale import gettext as _



st.set_page_config(page_title="Análise por aluno", page_icon="📈")

params = st.experimental_get_query_params()
schemaUsuario = params.get('usuario', ['moodle_marcio2'])[0]  
aluno = params.get('aluno', ['276'])[0]  

confs = Eny.secrets()

def dataFrame(aluno):


    from sqlalchemy import create_engine


    #st.write(confs) somente para debug não comitar essa linha descomentada =]
    
    # Recuperar os detalhes de conexão do banco de dados
    host = confs['connections']['postgresql']['host']
    database = confs['connections']['postgresql']['database']
    user = confs['connections']['postgresql']['username']
    password = confs['connections']['postgresql']['password']

    conn = create_engine(f"postgresql://{user}:{password}@{host}:5432/{database}")

    # Perform query.
    sql_query =  pd.read_sql_query (f"SELECT  nome_completo, texto_extraido, coh_frazier, coh_brunet, data_entrega, nota FROM {schemaUsuario}.tarefa_fato tf INNER JOIN {schemaUsuario}.aluno a ON a.id = tf.aluno_id WHERE aluno_id = {aluno};", con=conn)


    df = pd.DataFrame(sql_query, columns = ['titulo', 'nome_completo', 'texto_extraido', 'coh_frazier', 'coh_brunet', 'data_entrega', 'nota'])
    df["Year"] = df["data_entrega"].apply(lambda x: str(x.year) )
    df = df.sort_values("Year")


    return df

df = dataFrame(aluno)
st.dataframe(df)