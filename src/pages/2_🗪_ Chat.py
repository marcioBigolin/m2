import streamlit as st
import pandas as pd
import enyalius as eny

_ = eny.loadLang("Home", "pt-br")



def gepeto(  ):
    from pandasai import SmartDataframe
    from pandasai.llm.openai import OpenAI
    import matplotlib.pyplot as plt
    import os

    if "key" in eny.secrets()['openai']:
        st.session_state.openai_key = eny.secrets()['openai']['key']
        st.session_state.prompt_history = []


    if "openai_key" not in st.session_state:
        with st.form("API key"):
            key = st.text_input("OpenAI Key", value="", type="password")
            if st.form_submit_button(_("Enviar")):
                st.session_state.openai_key = key
                st.session_state.prompt_history = []
                st.success(_('API KEY Salva só alegria!')) #Validar entrada vazia

    #Para não precisar clicar 2x no botão
    if "openai_key" in st.session_state:
    
        with st.form("Question"):
            question = st.text_input(_("Digite aqui uma pergunta sobre os dados"), value="", type="default")
            submitted = st.form_submit_button(_("Gerar"))
            if submitted:
                with st.spinner():
                    llm = OpenAI(api_token=eny.secrets()['openai']['key'])
                    pandas_ai = SmartDataframe("./assets/demo.csv", config={
                    "llm": llm, 
                    "conversational": False, 
                    "enable_cache": True,
                    })

                    x = pandas_ai.chat(question)

                    if os.path.isfile('exports/charts/temp_chart.png'):
                        im = plt.imread('exports/charts/temp_chart.png')
                        st.image(im)
                        os.remove('exports/charts/temp_chart.png')

                    if x is not None:
                        st.write(x)

                    st.session_state.prompt_history.append(question)
    

        st.subheader(_("Prompt history:"))
        st.write(st.session_state.prompt_history)

        if "prompt_history" in st.session_state.prompt_history and len(st.session_state.prompt_history) > 0:
            if st.button(_("Limpar")):
                st.session_state.prompt_history = []
                st.session_state.df = None


st.header(_("IA Generativa"))
gepeto()