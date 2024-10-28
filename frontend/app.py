import streamlit as st
from rag import RAG
from maintenance_service import show_maintenance_service_panel
import os
from dotenv import load_dotenv
load_dotenv()

# Configuração da página
st.set_page_config(page_title="Dashboard de Ordem de Serviço de Manutenção", page_icon="🛠️", layout="wide")

# Título do sistema
st.title("🛠️ Sistema de Gerenciamento de Manutenção Magic Square")

# Barra lateral para navegação
st.sidebar.header("Navegação")

# Configuração de navegação na sessão
if "page" not in st.session_state:
    st.session_state["page"] = "Serviço de Manutenção"  # Página inicial

# Botões de navegação
if st.sidebar.button("Serviço de Manutenção"):
    st.session_state["page"] = "Serviço de Manutenção"
if st.sidebar.button("Inserir Tarefas"):
    st.session_state["page"] = "Inserir Tarefas"

rag = RAG()
docs = []
target_folder = '../data/documents/technical-catalog'
for file in os.listdir(target_folder):
    docs.append(f'{target_folder}/{file}')
rag.add_documents(docs)


# Controle de estado da sessão para detalhes
if "show_detail_page" not in st.session_state:
    st.session_state["show_detail_page"] = False
if "detail_content" not in st.session_state:
    st.session_state["detail_content"] = ""
if "task_status" not in st.session_state:
    st.session_state["task_status"] = {}

# Exibir painel com base na seleção
if st.session_state["page"] == "Serviço de Manutenção":
    show_maintenance_service_panel(rag)
elif st.session_state["page"] == "Inserir Tarefas":
    st.subheader("Inserir Nova Tarefa")
    
    # Botão para enviar áudio
    if st.button("Enviar Áudio"):
        st.write("Funcionalidade de envio de áudio em desenvolvimento.")

    # Caixa de texto para input de tarefas
    task_input = st.text_area("Descrição da Tarefa", placeholder="Digite a descrição da tarefa aqui...")
    
    # Botão para enviar a tarefa
    if st.button("Enviar Tarefa"):
        if task_input:
            st.success("Tarefa enviada com sucesso!")
        else:
            st.warning("Por favor, insira a descrição da tarefa antes de enviar.")
