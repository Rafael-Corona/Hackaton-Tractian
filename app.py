import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime

# Configurações da página
st.set_page_config(page_title="Dashboard de Ordem de Serviço de Manutenção", page_icon="🛠️", layout="wide")

# Título do dashboard
st.title("🛠️ Sistema de Gerenciamento de Manutenção Magic Square")

# Barra lateral com filtros e seleção de serviço de manutenção
st.sidebar.header("Navegação")
show_dashboard = st.sidebar.button("Dashboard")
show_maintenance_service = st.sidebar.button("Serviço de Manutenção")

# Inicializando estado da sessão para controle de navegação
if "show_detail_page" not in st.session_state:
    st.session_state.show_detail_page = False
if "detail_content" not in st.session_state:
    st.session_state.detail_content = ""

# Dados fictícios para exibição
data_size = 500

@st.cache_data
def generate_data(size):
    np.random.seed(42)
    data = pd.DataFrame({
        "ID Tarefa": range(1, size + 1),
        "Data de Criação": pd.date_range("2023-01-01", periods=size, freq="D"),
        "Status": np.random.choice(["Pendente", "Em Andamento", "Concluído"], size=size, p=[0.3, 0.5, 0.2]),
        "Tipo de Manutenção": np.random.choice(["Preventiva", "Corretiva", "Inspeção"], size=size),
        "Prioridade": np.random.choice(["Alta", "Média", "Baixa"], size=size)
    })
    return data

data = generate_data(data_size)

# Lógica de navegação entre abas
if show_dashboard:
    # Exibição do Dashboard
    st.subheader("Análise de Ordens de Serviço")

    # Gráfico de barras com contagem de tarefas por status
    st.markdown("### Tarefas por Status")
    status_counts = data['Status'].value_counts().reset_index()
    status_counts.columns = ["Status", "Quantidade"]
    status_chart = px.bar(status_counts, x="Status", y="Quantidade", title="Distribuição de Tarefas por Status")
    st.plotly_chart(status_chart, use_container_width=True)

    # Gráfico de pizza com tipos de manutenção
    st.markdown("### Tipos de Manutenção")
    maintenance_counts = data['Tipo de Manutenção'].value_counts().reset_index()
    maintenance_counts.columns = ["Tipo de Manutenção", "Quantidade"]
    maintenance_chart = px.pie(maintenance_counts, values="Quantidade", names="Tipo de Manutenção", title="Distribuição por Tipo de Manutenção")
    st.plotly_chart(maintenance_chart, use_container_width=True)

    # Métricas
    st.subheader("Métricas de Manutenção")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="Total de Tarefas", value=len(data))

    with col2:
        st.metric(label="Tarefas Pendentes", value=len(data[data["Status"] == "Pendente"]))

    with col3:
        st.metric(label="Tarefas Concluídas", value=len(data[data["Status"] == "Concluído"]))

elif show_maintenance_service or st.session_state.show_detail_page:
    if st.session_state.show_detail_page:
        # Página de detalhes com caixa de texto
        st.subheader("Detalhes do Serviço de Manutenção")
        st.text_area("Informações", st.session_state.detail_content, height=300)
        st.button("Voltar", on_click=lambda: setattr(st.session_state, "show_detail_page", False))
    else:
        # Função para definir conteúdo da página de detalhes e redirecionar
        def show_detail(content):
            st.session_state.detail_content = content
            st.session_state.show_detail_page = True

        # Página principal de Serviço de Manutenção
        st.subheader("Checklist de Serviços de Manutenção")

        # Exibição da data de hoje
        today = datetime.date.today()

        col1, col2 = st.columns([1, 1])
        with col1:
            st.button(f"Visualizar todas as ferramentas", on_click=show_detail, args=(f"Ferramentas necessárias para: ...",))
        with col2:
            st.button(f"Visualizar todos os manuais", on_click=show_detail, args=(f"Manual completo para: ...",))
        
        st.write(f"**Data de Hoje:** {today.strftime('%d/%m/%Y')}")

        # Lista de tarefas de manutenção
        maintenance_tasks = [
            "1. Verificar nível de óleo",
            "2. Inspecionar correias",
            "3. Limpeza de filtros",
            "4. Verificação de pressão dos pneus",
            "5. Teste de baterias",
            "6. Revisão de sistemas elétricos",
        ]

        # Status das tarefas e botões de ação
        task_status = {}

        for task in maintenance_tasks:
            task_status[task] = st.selectbox(f"{task} - Status", ["Não Realizado", "Em Andamento", "Concluído"])

            # Botões para visualizar ferramentas e manual
            col1, col2 = st.columns([1, 1])
            with col1:
                st.button(f"Visualizar Ferramentas - {task}", on_click=show_detail, args=(f"Ferramentas necessárias para {task}: ...",))
            with col2:
                st.button(f"Visualizar Manual - {task}", on_click=show_detail, args=(f"Manual completo para {task}: ...",))

# Rodapé
st.write("---")
st.caption("Dashboard de exemplo em Streamlit para gerenciamento de ordens de serviço de manutenção.")
