import json
from openai import OpenAI

def load_json_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

def gerar_checklist(client: OpenAI, transcribed_text: str) -> str:
    """
    Gera uma checklist a partir do texto transcrito.
    
    Args:
    client (OpenAI): Instância do cliente OpenAI.
    transcribed_text (str): Texto transcrito para gerar a checklist.

    Returns:
    str: A checklist gerada.
    """
    prompt = f"A partir do contexto e do texto transcrito a seguir, gere uma lista de verificação para o técnico de manutenção com todas as ações necessárias.\n\n"
    prompt += f"Texto transcrito:\n{transcribed_text}\n\n"
    prompt += f"""
    Por favor, organize as ações em uma checklist clara e específica. Gere o texto contendo o nome de uma tarefa da checklist, um item por linha, sem incluir números de linha.
    Exemplo de Formato Esperado:
    Tarefa 1: Nome da Tarefa
    Tarefa 2: Nome da Tarefa
    ...
    """

    # Call ChatGPT to generate the checklist
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é um assistente que ajuda a criar listas de verificação para manutenção com base em textos transcritos."},
            {"role": "user", "content": prompt}
        ],
    )

    # Extract and return the checklist text
    checklist = completion.choices[0].message.content
    return checklist

def gerar_equipamentos(client: OpenAI, data_lists: list, transcribed_text: str) -> str:
    """
    Gera uma lista de equipamentos necessários a partir da estrutura JSON usando o ChatGPT.

    Args:
    client (OpenAI): Instância do cliente OpenAI.
    data_lists (list): Lista de dicionários contendo as informações dos itens.

    Returns:
    str: Equipamentos necessários para cada tarefa.
    """
    # Cria o prompt em JSON
    json_data = json.dumps(data_lists, ensure_ascii=False)
    
    prompt = f"A partir da seguinte lista de itens em JSON, gere uma lista de equipamentos necessários para cada tarefa, {transcribed_text} na mesma ordem. Cada lista de equipamentos deve conter todas as ferramentas necessárias para a realização da tarefa correspondente.\n\n"
    prompt += f"Dados em JSON:\n{json_data}\n\n"
    
    # Call ChatGPT to generate the equipment list
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é um assistente que ajuda a criar listas de equipamentos necessários para tarefas."},
            {"role": "user", "content": prompt}
        ],
    )

    # Extract and return the equipment list text
    equipamentos = completion.choices[0].message.content
    return equipamentos

def generate_checklist(client: OpenAI, transcribed_text: str) -> str:
    """
    Função principal que combina a geração da checklist e dos equipamentos necessários.

    Args:
    client (OpenAI): Instância do cliente OpenAI.
    transcribed_text (str): Texto transcrito para gerar a checklist.

    Returns:
    str: A checklist junto com a lista de equipamentos necessários.
    """
    data_lists = load_json_data('backend/checklist/sap_codes.json')
    checklist = gerar_checklist(client, transcribed_text)
    equipamentos = gerar_equipamentos(client, data_lists, transcribed_text)
    
    # Combine both the checklist and the equipment list
    return f"{checklist}\n{equipamentos}"

'''
def generate_checklist(client: OpenAI, transcribed_text: str) -> str:
    data_lists = load_json_data('backend/checklist/sap_codes.json')
    # Define the prompt in Portuguese to ask for a checklist based on the transcribed text
    prompt = f"A partir do contexto e do texto transcrito a seguir, gere uma lista de verificação para o técnico de manutenção com todas as ações necessárias.\n\n"
    prompt += f"Texto transcrito:\n{transcribed_text}\n\n"
    prompt += f"""
    Por favor, organize as ações em uma checklist clara e específica. Gere o texto contendo o nome de uma tarefa da checklist, um item por linha, sem incluir números de linha.
    Após listar as tarefas, forneça uma lista de equipamentos necessários para cada tarefa, na mesma ordem em que as tarefas foram apresentadas. Cada lista de equipamentos deve conter todas as ferramentas necessárias para a realização da tarefa correspondente.
    Exemplo de Formato Esperado:
    Tarefa 1: Nome da Tarefa
    Tarefa 2: Nome da Tarefa
    ...
    /n/n
    Equipamentos Necessários para a tarefa 1: [lista de ferramentas]
    Equipamentos Necessários para a tarefa 2: [lista de ferramentas]
    ...

Nota: As listas devem ser completas e precisas, garantindo que cada tarefa tenha todos os equipamentos listados.

Por favor, considere um cenário de manutenção industrial ao gerar as tarefas e equipamentos.
    Use a seguinte lista de equipamentos com os seus respectivos codigos
    """
        # Acessando a estrutura correta do JSON
    if data_lists:  # Verifica se a lista não está vazia
        for lista in data_lists:  # Itera sobre a lista de dicionários
            titulo = lista.get('titulo', 'Título não disponível')  # Acessa o título
            prompt += f"{titulo}:\n"
            prompt += "| Categoria                  | Descrição                          | Código |\n"
            prompt += "|----------------------------|------------------------------------|--------|\n"
            for item in lista.get('itens', []):  # Acessando a lista de itens
                prompt += f"| {item.get('categoria', '')} | {item.get('descricao', '')} | {item.get('codigo', '')} |\n"
            prompt += "```\n\n"
    # Call ChatGPT to generate the checklist
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "system", "content": "Você é um assistente que ajuda a criar listas de verificação para manutenção com base em textos transcritos."},
                  {"role": "user", "content": prompt}],
    )
    
    # Extract and return the checklist text
    checklist = completion.choices[0].message.content
    return checklist
'''
