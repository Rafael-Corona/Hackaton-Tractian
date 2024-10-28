import json
from openai import OpenAI

def load_json_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

def generate_checklist(client: OpenAI, transcribed_text: str) -> str:
    data_lists = load_json_data('backend/checklist/sap_codes.json')
    # Define the prompt in Portuguese to ask for a checklist based on the transcribed text
    prompt = f"A partir do contexto e do texto transcrito a seguir, gere uma lista de verificação para o técnico de manutenção com as ações necessárias.\n\n"
    prompt += f"Texto transcrito:\n{transcribed_text}\n\n"
    prompt += f"""
    Por favor, organize as ações em uma checklist com pontos claros e específicos. Gere o texto em markdown.
    Além disso, gere uma checklist com os equipamentos necessarios para cada etapa.
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
    prompt += "Por favor, organize as ações em uma checklist com pontos claros e específicos. Gere o texto em markdown.\n"
    # Call ChatGPT to generate the checklist
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "system", "content": "Você é um assistente que ajuda a criar listas de verificação para manutenção com base em textos transcritos."},
                  {"role": "user", "content": prompt}],
    )
    
    # Extract and return the checklist text
    checklist = completion.choices[0].message.content
    return checklist
