import streamlit as st
import pandas as pd
import numpy as np

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

def load_maintenance_tasks(file_path):
    try:
        with open(file_path, "r") as file:
            tasks = [line.strip() for line in file if line.strip()]
        return tasks
    except FileNotFoundError:
        st.error("Arquivo de lista de tarefas não encontrado.")
        return []

def load_detail_content(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        st.error("Arquivo de conteúdo detalhado não encontrado.")
        return "Conteúdo não disponível."