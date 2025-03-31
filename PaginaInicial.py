import streamlit as st
from sqlalchemy import create_engine

st.set_page_config(
    page_title="Grupo Educacional Unis - Vagas de Emprego e Estágios", 
    page_icon="icone/icone.png", 
    layout="wide"
)

st.markdown(
    """
    <style>
        .stApp { background-color: #c0c0c0; }
        .stSidebar { background-color: #0b0b64 !important; }
        .stSidebar .sidebar-content { color: #0b0b64; }
        .stTitle{color:#000000; }
        .stHeader, .stText, .stMarkdown h1 { color: #11119c; }
        .stMarkdown p { color: #11119c; }
        .social-icons a { color: #11119c; text-decoration: none; padding: 5px; }
        .logo { position: absolute; top: 10px; left: 10px; width: 50px; }
        .stAppHeader{background-color: #0b0b64;}
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.image("logo/logo.png", width=100)

st.sidebar.title("Navegação")

pagina = st.sidebar.selectbox("Escolha uma página", ["Página Inicial"])

if pagina == "Página Inicial":
    st.title("Bem-vindo ao Nosso Site de Vagas de Emprego e Estágio")

st.sidebar.markdown("---")
st.sidebar.write("© 2025 Grupo Educacional Unis")

st.markdown(
    """
    <div class="social-icons">
        <a href="https://www.facebook.com/grupounis/#" target="_blank">Facebook</a>
        <a href="https://www.instagram.com/grupounis" target="_blank">Instagram</a>
        <a href="https://www.linkedin.com/school/grupounis/?originalSubdomain=br" target="_blank">LinkedIn</a>
        <a href="https://x.com/GrupoUnis" target="_blank">X</a>
    </div>
    """,
    unsafe_allow_html=True
)
