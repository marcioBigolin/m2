import streamlit as st
import pandas as pd
import os

#configure layout
st.set_page_config(page_title="MDI - Análise com IA", page_icon="🌍", layout="wide")
st.subheader("Explore os dados utilizando Inteligência artificial")
st.markdown("##")

def arquivoConf(nome_arquivo):
    arquivo_local = nome_arquivo.replace('.toml', '.local.toml')

    if os.path.isfile(arquivo_local):
        return arquivo_local
    else:
        return nome_arquivo


def dataFrame():
    # Recebe os parâmetros via GET enquanto sem criptografia mandando direto (usar bearertok)
    params = st.experimental_get_query_params()
    # Obtém o valor do parâmetro 'variavel' da URL
    schemaUsuario = params.get('usuario', ['SEM_DADOS'])[0]
    bd = params.get('banco', ['SEM_DADOS'])[0]

    from sqlalchemy import create_engine
    import toml


    # Caminho para o arquivo TOM    
    caminho_arquivo_tom = '.streamlit/secrets.toml'


    # Ler o arquivo TOM
    with open(caminho_arquivo_tom, 'r') as arquivo:
        dados = toml.load(arquivo)
    st.write(dados)
    # Recuperar os detalhes de conexão do banco de dados
    #host = dados['connections.postgresql']['host']
    #database = dados['connections.postgresql']['database']
    #user = dados['connections.postgresql']['usuario']
    #password = dados['connections.postgresql']['senha']

    conn = create_engine(f"postgresql://{user}:{password}@{host}:5432/{database}")

    # Perform query.
    sql_query =  pd.read_sql_query (f"SELECT * FROM {schemaUsuario}.fato_join;", con=conn)


    df = pd.DataFrame(sql_query, columns = ['titulo', 'nome_completo', 'coh_frazier', 'coh_brunet', 'data_entrega'])
    df["Year"] = df["data_entrega"].apply(lambda x: str(x.year) )
    df = df.sort_values("Year")

    # Criar uma seleção dos anos na barra lateral do dashboard
    st.sidebar.image("assets/logo.png", width=200)
    st.sidebar.title("Filtre os dados")
    years= st.sidebar.multiselect(
        'Quais anos deseja analizar?',
        options=df["Year"].unique(),
        default=df["Year"].unique())

    mask=df["Year"].isin(years)
    df=df[mask]

    return df




def gepeto():
    from pandasai import PandasAI
    from pandasai.llm.openai import OpenAI
    import matplotlib.pyplot as plt
    import os

    api_token = ""
    if "openai_key" not in st.session_state:
        with st.form("API key"):
            key = st.text_input("OpenAI Key", value="", type="password")
            if st.form_submit_button("Enviar"):
                st.session_state.openai_key = key
                st.session_state.prompt_history = []
                st.success('API KEY Salva só alegria!') #Validar entrada vazia

    #Para não precisar clicar 2x no botão
    if "openai_key" in st.session_state:
    
        with st.form("Question"):
            question = st.text_input("Question", value="", type="default")
            submitted = st.form_submit_button("Gerar")
            if submitted:
                with st.spinner():
                    llm = OpenAI(api_token=st.session_state.openai_key)
                    pandas_ai = PandasAI(llm)
                    x = pandas_ai.run(df, prompt=question)

                    if os.path.isfile('temp_chart.png'):
                        im = plt.imread('temp_chart.png')
                        st.image(im)
                        os.remove('temp_chart.png')

                    if x is not None:
                        st.write(x)

                    st.session_state.prompt_history.append(question)

    

        st.subheader("Prompt history:")
        st.write(st.session_state.prompt_history)

        if "prompt_history" in st.session_state.prompt_history and len(st.session_state.prompt_history) > 0:
            if st.button("Limpar"):
                st.session_state.prompt_history = []
                st.session_state.df = None

tab1, tab2, tab3 = st.tabs(["ChatGPT", "Gerador de gráfico", "Entendendo meus dados"])

df = dataFrame()

with tab1:
   st.header("IA Generativa")
   st.dataframe(df)
   gepeto()

with tab2:
    st.header("Modo clássico para a criação de gráficos")
    import pygwalker as pyg
    from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm
    # Establish communication between pygwalker and streamlit
    init_streamlit_comm()

    @st.cache_resource
    def get_pyg_renderer() -> "StreamlitRenderer":
        # When you need to publish your app to the public, you should set the debug parameter to False to prevent other users from writing to your chart configuration file.
        return StreamlitRenderer(df, spec="./gw_config.json", debug=False)
 
    renderer = get_pyg_renderer()
 
    # Render your data exploration interface. Developers can use it to build charts by drag and drop.
    renderer.render_explore()

with tab3:
    st.title("O MDI trabalha")
    st.text("teste ver se funciona com o Augusto")