import streamlit as st


params = st.experimental_get_query_params()
schemaUsuario = params.get('usuario', ['default'])[0]  


st.text(f"sds {schemaUsuario}")
