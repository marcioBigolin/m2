import enyalius as eny
import streamlit as st
import pandas as pd


st.set_page_config(page_title="Análise por aluno", page_icon="📈", layout="wide")

params = st.query_params
schemaUsuario = params.get('usuario', 'moodle_marcio2')  
aluno = params.get('aluno', '276')


def dataFrame(aluno):
    from sqlalchemy import text
    conn = eny.conecta()

    sqlw = f"SELECT  texto_extraido, coh_frazier, coh_brunet, data_entrega, nota FROM {schemaUsuario}.tarefa_fato tf INNER JOIN {schemaUsuario}.aluno a ON a.id = tf.aluno_id WHERE aluno_id = {aluno};"

    # Perform query.
    sql_query =  pd.read_sql_query(sql=text(sqlw), con=conn)
    df = pd.DataFrame(sql_query, columns = ['titulo', 'texto_extraido', 'coh_frazier', 'coh_brunet', 'data_entrega', 'nota'])

    return df

def dataTurma(aluno):
    conn = eny.conecta()

def dataMundo():
    from sqlalchemy import text
    conn = eny.conecta()

    sqlw = f"SELECT texto_extraido, coh_frazier, coh_brunet, data_entrega, nota, aluno_id FROM {schemaUsuario}.tarefa_fato WHERE LENGTH(texto_extraido) > 30;"

    # Perform query.
    sql_query =  pd.read_sql_query(sql=text(sqlw), con=conn)
    df = pd.DataFrame(sql_query, columns = ['titulo', 'texto_extraido', 'coh_frazier', 'coh_brunet', 'data_entrega', 'nota'])

    return df

st.title(f"Avaliação de {aluno}")

indiTab, turmaTab, mundoTab = st.tabs(["Individual", "Turma", "Mundo"])

with indiTab:
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

with mundoTab:
    df = dataMundo()
    df = pd.DataFrame(df[['coh_frazier']])  # Convert dictionary to DataFrame

    media = df['coh_frazier'].mean()


    df_line = pd.DataFrame({'x_line': [media]})

    st.vega_lite_chart(
    {"df": df, "df_line": df_line},
    {
        "layer": [{
            "data": {"name": "df"},
            "mark": "bar",
            "encoding": {
                "x": {"field": "coh_frazier", "bin": True},
                "y": {"aggregate": "count"}
            }
        },{
            "data": {"name": "df_line"},
            "mark": {
                "type": "rule",
                "strokeDash": [5, 5],
                "strokeWidth": 3
            },
            "encoding": {
                "x": {"field": "x_line"},
                "color": {"value": "red"}
            }
        }]
    }
    )