import streamlit as st
import Eny.confs as Eny
import Eny.decode as jwt


st.set_page_config(page_title="Análise por aluno", page_icon="📈")

params = st.experimental_get_query_params()
schemaUsuario = params.get('usuario', ['moodle_marcio2'])[0]  
aluno = params.get('aluno', ['SEM_DADOS'])[0]  

