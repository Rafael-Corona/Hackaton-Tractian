import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configurações da página
st.set_page_config(page_title="Dashboard de Ordem de Serviço de Manutenção", page_icon="🛠️", layout="wide")

# Título do dashboard
st.title("🛠️ Dashboard de Ordem de Serviço de Manutenção")

# Barra lateral com filtros
st.sidebar.header("Filtros")
data_size = st.sidebar.slider("Quantidade de Ordens de Serviço", 100, 1000, 500)
show_data = st.sidebar.checkbox("Mostrar dados")

# Gerando dados de exemplo para ordens de serviço
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

# Exibição de dados
if show_data:
    st.write("Ordens de Serviço:")
    st.dataframe(data)

# Gráficos
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

# Rodapé
st.write("---")
st.caption("Dashboard de exemplo em Streamlit para gerenciamento de ordens de serviço de manutenção.")

