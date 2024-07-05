import streamlit as st
import pandas as pd
import enyalius as eny

_ = eny.loadLang("Home", "pt-br")

st.set_page_config(page_title= _("MDI - Análise de dados"), page_icon="🏡", layout="wide")


def dataFrame():
    from sqlalchemy import text
    conn = eny.conecta()

    sqlw = f"SELECT * FROM {schemaUsuario}.fato_join;"

    # Perform query.
    sql_query =  pd.read_sql_query(sql=text(sqlw), con=conn)


    df = pd.DataFrame(sql_query, columns = ['titulo', 'nome_completo', 'coh_frazier', 'coh_brunet', 'data_entrega', 'id_tarefa', 'id_turma'])
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
    jwt = eny.decodeToken(data, confs['jwt'])

    st.text(jwt)

    schemaUsuario = st.query_params.get('usuario', 'SEM_DADOS')
except:
    if "schema" in eny.secrets()['dev']:
        schemaUsuario = eny.secrets()['dev']['schema']
    else:
        schemaUsuario = "SEM_DADOS"


if schemaUsuario == 'SEM_DADOS':
    st.subheader(_("Modo Inválido"))
    st.markdown(f"{_('Acesse pelo site do')} [MDI]({confs['geral']['mdilink']})")
else:

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

    tab1, tab2, tab3 = st.tabs([_("Dashboard"), _("Gerador de gráfico"), _("Entendendo meus dados")])
    

    with tab1:
        st.title(_("Resumo"))
        st.write(_("Pequeno resumo dos dados importados pelo MDI."))

        from datetime import datetime, timedelta
        data_atual = datetime.now() - timedelta(days=660)
        dfFilter =  df.loc[df['data_entrega'] >= data_atual]

        cols = st.columns(3)
        cols[0].metric(_("Estudantes"), df["nome_completo"].nunique(), dfFilter["nome_completo"].nunique())
        cols[1].metric(_("Atividades"), "9 mph", "-8%")
        cols[2].metric("Turmas acompanhadas", "86%", "4%")

    with tab2:
        st.header(_("Modo clássico para a criação de gráficos"))
        pygwalker(df)

    with tab3:
        st.title(_("Como analisar o dados no MDI/MDA"))
        st.markdown(_("O MDI utiliza um modelo estrela (Kimball/Imon) clássico. O que significa que o modelo foi reestruturado para consulta."))
        st.dataframe(df)