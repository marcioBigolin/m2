import streamlit as st
import pandas as pd
from locale import gettext as _

import enyalius as eny


st.set_page_config(page_title="Análise por aluno", page_icon="📈", layout="wide")

params = st.experimental_get_query_params()
schemaUsuario = params.get('usuario', ['moodle_marcio2'])[0]  
aluno = params.get('aluno', ['276'])[0]  




def dataFrame(aluno):

    conn = eny.conecta()

    # Perform query.
    sql_query =  pd.read_sql_query (f"SELECT  texto_extraido, coh_frazier, coh_brunet, data_entrega, nota FROM {schemaUsuario}.tarefa_fato tf INNER JOIN {schemaUsuario}.aluno a ON a.id = tf.aluno_id WHERE aluno_id = {aluno};", con=conn)


    df = pd.DataFrame(sql_query, columns = ['titulo', 'texto_extraido', 'coh_frazier', 'coh_brunet', 'data_entrega', 'nota'])
    df["Year"] = df["data_entrega"].apply(lambda x: str(x.year) )
    df = df.sort_values("Year")
    return df

def dataTurma(aluno):
    conn = eny.conecta()

st.title(f"Avaliação de {aluno}")

tab1, tab2, tab3 = st.tabs(["Individual", "Turma", "Mundo"])

df = dataFrame(aluno)
col1, col2 = st.columns([8, 4])
with col1:
    st.header("Últimos registros")
    st.dataframe(df.head(10))
with col2:
    st.header("Resumo")
    st.write(df.describe()) # ver de transformar isso em métricas



chart_data = df[['coh_frazier', 'coh_brunet']]

st.bar_chart(chart_data)