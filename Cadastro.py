import re
import sqlite3

import bcrypt
import streamlit as st

st.markdown("""
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
""", unsafe_allow_html=True)

def conectar_db():
    conn = sqlite3.connect('banco_unis.db')
    cursor = conn.cursor()
    return conn, cursor

def criar_tabelas():
    conn, cursor = conectar_db()

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS alunos (
            id_aluno INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_completo TEXT NOT NULL,
            ra TEXT UNIQUE NOT NULL,
            cpf TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            curso TEXT NOT NULL,      -- Novo campo para curso
            periodo TEXT NOT NULL,    -- Novo campo para período
            cidade TEXT NOT NULL      -- Novo campo para cidade
        );
    ''')

    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS empresas (
            id_empresa INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_empresa TEXT NOT NULL,
            cnpj TEXT UNIQUE NOT NULL,
            localizacao TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        );
    ''')

    conn.commit()
    conn.close()
st.sidebar.image("logo.png", width=100)
st.sidebar.title("Navegação")
pagina = st.sidebar.selectbox("Escolha uma página", ["Página Inicial", "Cadastro de Aluno", "Cadastro de Empresa", "Login", "Área da Conta"])

def cadastro_aluno():
    st.title("Cadastro de Aluno")
    nome_completo = st.text_input("Nome Completo")
    ra = st.text_input("RA")
    cpf = st.text_input("CPF")
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")
    curso = st.text_input("Curso")          # Novo campo para o curso
    periodo = st.text_input("Período")      # Novo campo para o período
    cidade = st.text_input("Cidade")        # Novo campo para a cidade

    if st.button("Cadastrar Aluno"):
        if nome_completo and ra and cpf and email and senha and curso and periodo and cidade:
            conn, cursor = conectar_db()
            cursor.execute("SELECT COUNT(*) FROM alunos WHERE email = ?", (email,))
            if cursor.fetchone()[0] > 0:
                st.error("Este e-mail já está cadastrado!")
            else:
                hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
                cursor.execute(''' 
                    INSERT INTO alunos (nome_completo, ra, cpf, email, senha, curso, periodo, cidade) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (nome_completo, ra, cpf, email, hashed_password, curso, periodo, cidade))
                conn.commit()
                st.success("Cadastro realizado com sucesso!")
            conn.close()
        else:
            st.error("Por favor, preencha todos os campos.")
def cadastro_empresa():
    st.title("Cadastro de Empresa")
    nome_empresa = st.text_input("Nome da Empresa")
    cnpj = st.text_input("CNPJ")
    localizacao = st.text_input("Localização")
    telefone = st.text_input("Telefone")
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")
    
    if st.button("Cadastrar Empresa"):
        if nome_empresa and cnpj and localizacao and telefone and email and senha:
            hashed_password = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
            conn, cursor = conectar_db()
            cursor.execute(''' 
                INSERT INTO empresas (nome_empresa, cnpj, localizacao, telefone, email, senha)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome_empresa, cnpj, localizacao, telefone, email, hashed_password))
            conn.commit()
            st.success("Cadastro realizado com sucesso!")
            conn.close()
        else:
            st.error("Por favor, preencha todos os campos.")

def login():
    email = st.text_input("Digite seu e-mail")
    senha_informada = st.text_input("Digite sua senha", type="password")

    if st.button("Login"):
        conn, cursor = conectar_db()

        # Verifica se é um aluno
        cursor.execute("SELECT nome_completo, senha FROM alunos WHERE email = ?", (email,))
        resultado_aluno = cursor.fetchone()

        # Verifica se é uma empresa
        cursor.execute("SELECT nome_empresa, senha FROM empresas WHERE email = ?", (email,))
        resultado_empresa = cursor.fetchone()

        if resultado_aluno:
            nome, senha_hash = resultado_aluno
            if bcrypt.checkpw(senha_informada.encode('utf-8'), senha_hash):
                st.success(f"Login bem-sucedido como Aluno: {nome}!")
                st.session_state.user_type = 'aluno'
                st.session_state.email = email
                st.session_state.nome = nome  # Guarda o nome do usuário
            else:
                st.error("Senha incorreta para o aluno!")
        elif resultado_empresa:
            nome, senha_hash = resultado_empresa
            if bcrypt.checkpw(senha_informada.encode('utf-8'), senha_hash):
                st.success(f"Login bem-sucedido como Empresa: {nome}!")
                st.session_state.user_type = 'empresa'
                st.session_state.email = email
                st.session_state.nome = nome  # Guarda o nome da empresa
            else:
                st.error("Senha incorreta para a empresa!")
        else:
            st.error("E-mail não encontrado!")
        conn.close()
        if "nome" in st.session_state:
            st.sidebar.markdown(f"**Usuário logado:** {st.session_state.nome}")
# Exibir conteúdo com base na seleção
if pagina == "Página Inicial":
    st.title("Bem-vindo ao Grupo Educacional Unis")
    st.write("Selecione uma opção no menu lateral para realizar o cadastro ou login.")
elif pagina == "Cadastro de Aluno":
    cadastro_aluno()
elif pagina == "Cadastro de Empresa":
    cadastro_empresa()
elif pagina == "Login":
    login()
st.sidebar.markdown("---")
st.sidebar.write("© 2025 Grupo Educacional Unis")

st.markdown("""
    <div class="social-icons">
        <a href="https://www.facebook.com/grupounis/#" target="_blank">Facebook</a>
        <a href="https://www.instagram.com/grupounis" target="_blank">Instagram</a>
        <a href="https://www.linkedin.com/school/grupounis/?originalSubdomain=br" target="_blank">LinkedIn</a>
        <a href="https://x.com/GrupoUnis" target="_blank">X</a>
    </div>
""", unsafe_allow_html=True)

criar_tabelas()
