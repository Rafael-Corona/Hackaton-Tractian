import streamlit as st
import datetime
from utils import load_maintenance_tasks, load_detail_content

# Função para exibir o painel de serviço de manutenção
def show_maintenance_service_panel(rag):
    # Inicializar session state
    if "show_detail_page" not in st.session_state:
        st.session_state["show_detail_page"] = False
    if "detail_content" not in st.session_state:
        st.session_state["detail_content"] = ""
    if "task_status" not in st.session_state:
        st.session_state["task_status"] = {}

    # Verifica se a página de detalhes está ativa
    if st.session_state["show_detail_page"]:
        # Página de detalhes com conteúdo somente leitura
        st.subheader("Detalhes do Serviço de Manutenção")
        st.text_area("Informações", st.session_state["detail_content"], height=300, disabled=True)
        if st.button("Voltar"):
            st.session_state["show_detail_page"] = False  # Retorna à página anterior
    else:
        # Função para definir conteúdo da página de detalhes
        def show_detail(content_file):
            st.session_state["detail_content"] = load_detail_content(content_file)
            st.session_state["show_detail_page"] = True

        # Função para definir conteúdo da página de detalhes
        def mostra_manual(string):
            st.session_state["detail_content"] = string
            st.session_state["show_detail_page"] = True

        # Exibir data de hoje e lista de tarefas
        st.subheader("Checklist de Serviços de Manutenção")
        today = datetime.date.today()
        st.write(f"**Data de Hoje:** {today.strftime('%d/%m/%Y')}")

        # Exibir botões para visualizar todas as ferramentas e manuais
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Visualizar todas as Ferramentas"):
                show_detail("data/tarefas/tasks.txt")
        with col2:
            if st.button("Visualizar todos os Manuais"):
                #chamar outra função aqui
                mostra_manual(rag.query("What is the best option to maintain energy supply?"))

        # Carregar tarefas do arquivo
        tasks_file_path = "data/tarefas/tasks.txt"
        maintenance_tasks = load_maintenance_tasks(tasks_file_path)

        # Exibir status de cada tarefa e botões de ação
        for task in maintenance_tasks:
            # Inicializa o status da tarefa, se ainda não estiver no session_state
            if task not in st.session_state["task_status"]:
                st.session_state["task_status"][task] = "Não Realizado"

            # Seletor de status da tarefa
            st.session_state["task_status"][task] = st.selectbox(
                f"{task} - Status",
                ["Não Realizado", "Em Andamento", "Concluído"],
                index=["Não Realizado", "Em Andamento", "Concluído"].index(st.session_state["task_status"][task]),
                key=task
            )

            # Botões de detalhes
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"Visualizar Ferramentas - {task}", key=f"tools_button_{task}"):
                    show_detail(f"data/ferramentas/ferramentas_{task}.txt")
            with col2:
                if st.button(f"Visualizar Manual - {task}", key=f"manual_button_{task}"):
                    show_detail(f"data/manuais/manual_{task}.txt")
