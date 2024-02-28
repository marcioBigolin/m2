import streamlit as st
import pandas as pd
import enyalius as eny
from locale import gettext as _


def dataFrame():
    conn=eny.conecta()

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
    from pygwalker.api.streamlit import StreamlitRenderer, init_streamlit_comm  

    init_streamlit_comm()
  
    # Get an instance of pygwalker's renderer. You should cache this instance to effectively prevent the growth of in-process memory.
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

confs = eny.secrets()

if schemaUsuario == 'SEM_DADOS':
    st.subheader(_("Modo Inválido"))
    st.markdown(f"Acesse pelo site do [MDI]({confs['geral']['mdilink']})")


else:

    df = dataFrame()


    #configure layout
    st.set_page_config(page_title= _("MDI - Análise com AI"), page_icon="🏡", layout="wide")
    st.subheader(_("Explore os dados utilizando Inteligência artificial"))
    st.markdown("##")

    # Criar uma seleção dos anos na barra lateral do dashboard
    st.sidebar.title("Filtre os dados")
    years= st.sidebar.multiselect(
        _('Quais anos deseja analizar?'),
        options=df["Year"].unique(),
        default=df["Year"].unique())

    mask=df["Year"].isin(years)
    df=df[mask]
    st.sidebar.image("./assets/logo.png", width=200)

    tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "ChatGPT", "Gerador de gráfico", "Entendendo meus dados"])

    df = dataFrame()

    with tab1:
        st.title("Resumo")
        st.text("Esse painel apresentamos os dados mais comuns das suas turmas.")

        cols = st.columns(3)
        cols[0].metric("Total de estudantes", "70 °F", "1.2 °F")
        cols[1].metric("Wind", "9 mph", "-8%")
        cols[2].metric("Humidity", "86%", "4%")

    with tab2:
        st.header("IA Generativa")
        st.dataframe(df)
        gepeto()

    with tab3:
        st.header("Modo clássico para a criação de gráficos")
        pygwalker()

    with tab4:
        st.title("Como analisar o dados no MDI/MDA")
        st.text("O MDI utiliza um modelo estrela (Kimball/Imon) clássico. O que significa que o modelo foi reestruturado para consulta.")
