import enyalius as eny
import streamlit as st
import pandas as pd

_ = eny.loadLang("Home", "pt-br")


st.set_page_config(page_title="Análise por aluno", page_icon="📈", layout="wide")

params = st.query_params
schemaUsuario = params.get('usuario', 'moodle_marcio2')  
aluno = params.get('aluno', 101)


def dataMundo():
    from sqlalchemy import text
    conn = eny.conecta()

    sqlw = f"SELECT texto_extraido, coh_frazier, coh_brunet, data_entrega, nota, turma_id, aluno_id, nome_completo FROM {schemaUsuario}.tarefa_fato tf INNER JOIN {schemaUsuario}.aluno a ON a.id = aluno_id WHERE LENGTH(texto_extraido) > 30;"

    # Perform query.
    sql_query =  pd.read_sql_query(sql=text(sqlw), con=conn)
    df = pd.DataFrame(sql_query, columns = ['titulo', 'texto_extraido', 'coh_frazier', 'coh_brunet', 'data_entrega', 'nota', 'nome_completo', 'aluno_id'])

    return df

def analiseMetrica(data):



    col1, col2 = st.columns([4, 8])
    with col1:
        import requests

        metrica_sem_prefixo = metrica.replace('coh_', '')

        # Faça uma solicitação GET para buscar a descrição da métrica
        response = requests.get(f'https://revisaoonline.com.br/public/verMetrica/{metrica_sem_prefixo}')

        if response.status_code == 200:
            st.markdown(response.content.decode() , unsafe_allow_html= True)
    with col2:
  
        media = df[metrica].mean()

        import plotly.graph_objects as go

        fig = go.Figure()
        fig.add_trace(go.Histogram(x=data[metrica]))

        fig.add_shape(
            type="line",
            x0=media,
            x1=media,
            y0=0,
            y1=1,
            yref="paper",
            line=dict(
                color="Red",
                width=3,
                dash="dashdot",
            )
        )

        st.plotly_chart(fig)
        st.write('A análise de histograma e gráfico mostra que a média da métrica é: ', media)




dfMundo= dataMundo()



# Cria um dicionário onde as chaves são os IDs dos alunos e os valores são os nomes dos alunos
alunos_dict = pd.Series(dfMundo.nome_completo.values,index=dfMundo.aluno_id).to_dict()



st.sidebar.title(_("Filtre os dados"))
keys_list = list(alunos_dict.keys())
aluno_index = keys_list.index(int(aluno))

aluno = st.sidebar.selectbox(
        _('Selecione um aluno para continuar?'),
        options=keys_list,
        index=aluno_index,
        format_func=lambda x: alunos_dict[x]
)
df = dfMundo.loc[dfMundo['aluno_id'] == aluno]

# Mapeamento de valores internos para rótulos
mapa_rotulos = {
    'coh_frazier': 'Complexidade Sintática de Frazier',
    'coh_brunet': 'Indice de Brunet',
}

# Inverta o dicionário para mapear rótulos para valores internos
mapa_valores = {v: k for k, v in mapa_rotulos.items()}

# Use os rótulos no selectbox
rotulo_selecionado = st.sidebar.selectbox(
    'Por favor, selecione a métrica que deseja visualizar:',
    list(mapa_rotulos.values())
)

# Mapeie o rótulo de volta para o valor interno
metrica = mapa_valores[rotulo_selecionado]

st.title(f"Avaliação de {alunos_dict[aluno]}")

indiTab, turmaTab, mundoTab = st.tabs(["Individual", "Turma", "Mundo"])

with indiTab:
    

    st.line_chart(df[[metrica, 'data_entrega']], x='data_entrega', y=metrica)

    col1, col2 = st.columns([8, 4])
    with col1:
        st.header("Últimos registros")
        st.dataframe(df.head(10))
    with col2:
        st.header("Resumo")
        st.write(df.describe()) # ver de transformar isso em métricas

 

with turmaTab:
    st.header("Análise de métricas por turma")
    # data = dataTurma(aluno)
    # analiseMetrica(data)

with mundoTab:
    analiseMetrica(dfMundo)
