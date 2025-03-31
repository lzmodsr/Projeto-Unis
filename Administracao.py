import mysql.connector
import pandas as pd
import streamlit as st

st.markdown(
    """
    <style>
        .stApp { background-color: #c0c0c0; }
        .stSidebar { background-color: #0b0b64 !important; }
        .stSidebar .sidebar-content { color: #ffffff; }
        .stTitle { color: #000000; }
        .stHeader, .stText, .stMarkdown h1 { color: #11119c; }
        .stMarkdown p { color: #11119c; }
        .social-icons a { color: #11119c; text-decoration: none; padding: 5px; }
        .logo { position: absolute; top: 10px; left: 10px; width: 50px; }
        .stAppHeader{background-color: #0b0b64;}
    </style>
    """,
    unsafe_allow_html=True,
)
def get_connection():
    """Estabelece a conexão com o banco de dados MySQL."""
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=8501,  # Porta padrão do MySQL
            user="Unis",
            password="unis2025",
            database="banco_unis.db"
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Erro ao conectar ao banco de dados: {err}")
        return None

def get_data(query):
    conn = get_connection()
    if conn is None:
        return pd.DataFrame()
    
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query)
        data = cursor.fetchall()
        return pd.DataFrame(data)
    except mysql.connector.Error as err:
        st.error(f"Erro ao buscar dados: {err}")
        return pd.DataFrame()
    finally:
        conn.close()
st.sidebar.image("logo/logo.png", width=100)
# Interface do aplicativo
st.title("Painel de Administração")
menu = ["alunos", "empresas", "vagas", "candidaturas"]
opcao = st.sidebar.selectbox("Selecione a tabela", menu)

# Botão para atualizar os dados
if st.sidebar.button("Atualizar Dados"):
    st.rerun()

tabelas = {
    "alunos": "SELECT * FROM alunos",
    "empresas": "SELECT * FROM empresas",
    "vagas": "SELECT * FROM vagas",
    "candidaturas": "SELECT * FROM candidaturas"
}

if opcao in tabelas:
    st.subheader(f"Tabela de {opcao}")
    df = get_data(tabelas[opcao])
    if not df.empty:
        st.dataframe(df)
    else:
        st.warning("Nenhum dado encontrado.")
