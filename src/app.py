import streamlit as st
import pandas as pd
import Eny.confs as Eny



def dataFrame():


    from sqlalchemy import create_engine


    #st.write(confs) somente para debug não comitar essa linha descomentada =]
    
    # Recuperar os detalhes de conexão do banco de dados
    host = confs['connections']['postgresql']['host']
    database = confs['connections']['postgresql']['database']
    user = confs['connections']['postgresql']['username']
    password = confs['connections']['postgresql']['password']

    conn = create_engine(f"postgresql://{user}:{password}@{host}:5432/{database}")

    # Perform query.
    sql_query =  pd.read_sql_query (f"SELECT * FROM {schemaUsuario}.fato_join;", con=conn)


    df = pd.DataFrame(sql_query, columns = ['titulo', 'nome_completo', 'coh_frazier', 'coh_brunet', 'data_entrega'])
    df["Year"] = df["data_entrega"].apply(lambda x: str(x.year) )
    df = df.sort_values("Year")





    return df


def gepeto():
    from pandasai import SmartDataframe
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
                    pandas_ai = SmartDataframe(llm)
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


def pygwalker():
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

#############################

# Recebe os parâmetros via GET enquanto sem criptografia mandando direto (usar bearertok)
params = st.experimental_get_query_params()
# Obtém o valor do parâmetro 'variavel' da URL
schemaUsuario = params.get('usuario', ['SEM_DADOS'])[0]  

confs = Eny.secrets()

if schemaUsuario == 'SEM_DADOS':
    st.subheader("Modo Inválido")
    st.write(f"Acesse pelo site do MDI: <a href='{confs['geral']['mdilink']}'>MDI</a>", unsafe_allow_html=True)

else:

    df = dataFrame()


    #configure layout
    st.set_page_config(page_title="MDI - Análise com IA", page_icon="🌍", layout="wide")
    st.subheader("Explore os dados utilizando Inteligência artificial")
    st.markdown("##")

    # Criar uma seleção dos anos na barra lateral do dashboard
    st.sidebar.image("./assets/logo.png", width=200)
    st.sidebar.title("Filtre os dados")
    years= st.sidebar.multiselect(
        'Quais anos deseja analizar?',
        options=df["Year"].unique(),
        default=df["Year"].unique())

    mask=df["Year"].isin(years)
    df=df[mask]

    tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "ChatGPT", "Gerador de gráfico", "Entendendo meus dados"])

    df = dataFrame()

    with tab1:
        st.title("Resumo")
        st.text("Esse painel apresentamos os dados mais comuns das suas turmas.")

    with tab2:
        st.header("IA Generativa")
        st.dataframe(df)
        gepeto()

    with tab3:
        st.header("Modo clássico para a criação de gráficos")
        pygwalker()

    with tab4:
        st.title("O MDI trabalha")
        st.text("teste ver se funciona com o Augusto")