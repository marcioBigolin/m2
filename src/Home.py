import streamlit as st
import pandas as pd
import enyalius as eny

_ = eny.loadLang("Home", "pt-br")

st.set_page_config(page_title= _("MDI - Análise de dados Textuais"), page_icon="🏡", layout="wide")


def dataFrame():
    from sqlalchemy import text
    conn, engine = eny.conecta()

    sqlw = f"SELECT * FROM {schemaUsuario}.fato_join;"
    print(sqlw)

    # Perform query.
    sql_query =  pd.read_sql_query(sql=text(sqlw), con=conn)


    df = pd.DataFrame(sql_query, columns = ['titulo', 'nome_completo', 'coh_frazier', 'coh_brunet', 'data_entrega', 'id_tarefa', 'id_turma'])
    eny.desconecta(conn, engine)

    # Alterando os rótulos das colunas
        

    df["Year"] = df["data_entrega"].apply(lambda x: str(x.year) )
    df = df.sort_values("Year")


    return df


def pygwalker(df):
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

confs = eny.secrets()

try:
    data = eny.GET('encode')
    jwt = eny.decodeToken(data, confs['geral']['jwt'])   
    schemaUsuario = 'moodle_' + eny.decriptaAES(jwt['data']['schema'], confs['geral']['jwt'])
except Exception as e:
    st.text(e)
    if "schema" in eny.secrets()['dev']:
        schemaUsuario = eny.secrets()['dev']['schema'] 
    else:
        schemaUsuario = "SEM_DADOS"


if schemaUsuario == 'SEM_DADOS':
    st.subheader(_("Modo Inválido"))
    st.markdown(f"{_('Acesse pelo site do')} [MDI]({confs['geral']['mdilink']})")
else:
    st.text(schemaUsuario)
    df = dataFrame()


    #configure layout
    st.subheader(_("Explore os dados atráves do Dashboard interativo"))
    st.markdown("##")

    # # Criar uma seleção dos anos na barra lateral do dashboard
    # st.sidebar.title(_("Filtre os dados"))
    # years= st.sidebar.multiselect(
    #     _('Quais anos deseja analizar?'),
    #     options=df["Year"].unique(),
    #     default=df["Year"].unique())

    # mask=df["Year"].isin(years)
    # df=df[mask]
    st.sidebar.image("./assets/logo.png", width=200)
    st.sidebar.markdown(f"<a href='{confs['geral']['mdilink']}'>[Acessar importação]<a>", True)

    tab1, tab2, tab3 = st.tabs([_("Dashboard"), _("Gerador de gráfico"), _("Entendendo meus dados")])
    

    with tab1:
        st.title(_("Resumo"))
        st.write(_("Pequeno resumo dos dados textuais importados pelo MDI."))

        from datetime import datetime, timedelta
        data_atual = datetime.now() - timedelta(days=660)
        dfFilter =  df.loc[df['data_entrega'] >= data_atual]

        cols = st.columns(3)
        cols[0].metric(_("Estudantes"), df["nome_completo"].nunique(), dfFilter["nome_completo"].nunique())
        cols[1].metric(_("Atividades"), df["titulo"].nunique(), dfFilter["titulo"].nunique())
        cols[2].metric("Turmas acompanhadas", "0", "0")

    with tab2:
        st.header(_("Modo clássico para a criação de gráficos"))
        pygwalker(df)

    with tab3:
        st.title(_("Como analisar o dados no MDI/MDA"))
        st.markdown(_("O MDI utiliza um modelo estrela (Kimball/Imon) clássico. O que significa que o modelo foi reestruturado para consulta. "))
        st.markdown(_("Basicamente os dados importados ficam na estrutura abaixo como você pode analisar"))

        df.columns = ['Tema', 'Nome do aluno', 'Indice Frazier', 'Indice Brunet', 'data_entrega', 'Task ID', 'Class ID', 'ano']
        st.dataframe(df)