import sqlite3

import streamlit as st

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

# Função para conectar ao banco de dados SQLite
def connect_db():
    conn = sqlite3.connect('banco_unis.db')
    return conn

st.sidebar.image("logo/logo.png", width=100)

# Função para criar as tabelas necessárias
def create_tables():
    conn = connect_db()
    c = conn.cursor()
    c.execute('''  
        CREATE TABLE IF NOT EXISTS vagas (
            id_vaga INTEGER PRIMARY KEY AUTOINCREMENT,
            id_empresa INTEGER,
            nome_empresa TEXT,
            link_site TEXT,
            area_trabalho TEXT,
            tempo_trabalho TEXT,
            localizacao TEXT,
            valor_salarial DECIMAL(10, 2),
            telefone_contato TEXT,
            status TEXT CHECK(status IN ('pendente', 'aprovada', 'rejeitada'))
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS candidaturas (
            id_candidatura INTEGER PRIMARY KEY AUTOINCREMENT,
            id_aluno INTEGER,
            id_vaga INTEGER,
            curriculo TEXT,
            FOREIGN KEY (id_vaga) REFERENCES vagas(id_vaga)
        )
    ''')
    conn.commit()
    conn.close()

def listar_vagas():
    conn = connect_db()
    c = conn.cursor()
    c.execute('SELECT * FROM vagas WHERE status = "aprovada"')
    vagas = c.fetchall()
    conn.close()
    return vagas

def cadastrar_vaga(id_empresa, area_trabalho, tempo_trabalho, localizacao, valor_salarial, telefone_contato, status):
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO vagas (id_empresa, area_trabalho, tempo_trabalho, localizacao, valor_salarial, telefone_contato, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (id_empresa, area_trabalho, tempo_trabalho, localizacao, valor_salarial, telefone_contato, status))
    conn.commit()
    conn.close()
    st.success("Vaga cadastrada com sucesso!")

def excluir_vaga(id_vaga):
    conn = connect_db()
    c = conn.cursor()
    c.execute('DELETE FROM vagas WHERE id_vaga = ?', (id_vaga,))
    conn.commit()
    conn.close()
    st.success(f"Vaga {id_vaga} excluída com sucesso!")

def candidatar_vaga(id_aluno, id_vaga, curriculo):
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO candidaturas (id_aluno, id_vaga, curriculo)
        VALUES (?, ?, ?)
    ''', (id_aluno, id_vaga, curriculo))
    conn.commit()
    conn.close()
    st.success(f'Candidatura para a vaga {id_vaga} realizada com sucesso!')

def main():
    st.title("Cadastro de Vagas e Candidaturas")
    create_tables()
    # Formulário de cadastro de vaga
    st.subheader("Cadastrar Nova Vaga")
    with st.form(key='form_vaga'):
        id_empresa = st.number_input('ID da Empresa', min_value=1, step=1)
        nome_empresa = st.text_input('Nome da Empresa')  # Novo campo
        link_site = st.text_input('Link do Site da Empresa')  # Novo campo
        area_trabalho = st.text_input('Área de Trabalho')
        tempo_trabalho = st.text_input('Tempo de Trabalho')
        localizacao = st.text_input('Localização')
        valor_salarial = st.number_input('Valor Salarial', min_value=0.0, step=0.01)
        telefone_contato = st.text_input('Telefone de Contato')
        status = st.selectbox('Status', ['pendente', 'aprovada', 'rejeitada'])

        submit_button = st.form_submit_button(label='Cadastrar Vaga')
        if submit_button:
            if area_trabalho and tempo_trabalho and localizacao and telefone_contato:
                cadastrar_vaga(id_empresa, nome_empresa, link_site, area_trabalho, tempo_trabalho, localizacao, valor_salarial, telefone_contato, status)
            else:
                st.error('Por favor, preencha todos os campos obrigatórios!')

    st.subheader("Vagas Disponíveis")
    vagas = listar_vagas()
    
    if vagas:
        for vaga in vagas:
            st.write(f"**Área de Trabalho**: {vaga[2]}")
            st.write(f"**Tempo de Trabalho**: {vaga[3]}")
            st.write(f"**Localização**: {vaga[4]}")
            st.write(f"**Valor Salarial**: R$ {vaga[5]:.2f}")
            st.write(f"**Telefone de Contato**: {vaga[6]}")

            # Formulário para exclusão de vaga
            excluir_button = st.button(f"Excluir Vaga {vaga[0]}", key=f"excluir_{vaga[0]}")
            if excluir_button:
                confirmar = st.radio(
                    f"Tem certeza que deseja excluir a vaga {vaga[0]}?", 
                    ['Não', 'Sim'], 
                    key=f"confirmar_excluir_{vaga[0]}"
                )
                if confirmar == 'Sim':
                    excluir_vaga(vaga[0])
                    st.experimental_rerun()  # Recarrega a aplicação para atualizar a lista de vagas
                elif confirmar == 'Não':
                    st.info("Exclusão cancelada.")

            with st.form(key=f'form_candidatura_{vaga[0]}'):
                id_aluno = st.number_input('ID do Aluno', min_value=1, step=1, key=f'id_aluno_{vaga[0]}')
                curriculo = st.text_input("Link do Currículo (PDF) ", key=f'curriculo_{vaga[0]}')
                submit_button = st.form_submit_button(label=f'Candidatar para a vaga {vaga[0]}')

                if submit_button:
                    if id_aluno and curriculo:
                        candidatar_vaga(id_aluno, vaga[0], curriculo)
                    else:
                        st.error('Preencha todos os campos corretamente!')
st.markdown("""
    <div class="social-links">
        <a href="https://www.facebook.com/grupounis/#" target="_blank">Facebook</a>
        <a href="https://www.instagram.com/grupounis" target="_blank">Instagram</a>
        <a href="https://www.linkedin.com/school/grupounis/?originalSubdomain=br" target="_blank">LinkedIn</a>
        <a href="https://x.com/GrupoUnis" target="_blank">X</a>
    </div>
""", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
