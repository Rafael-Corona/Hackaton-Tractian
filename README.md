# Gerador de Checklist para Manutenção Industrial Magic Square

Este projeto consiste em um gerador de listas de verificação (checklists) para auxiliar técnicos de manutenção industrial. 
O programa oferece a funcionalidade de converter áudio em texto usando inteligencia artificial e gera checklists baseados tanto em entradas de áudio quanto em texto corrido. Utiliza a API da OpenAI para gerar as listas de verificação e o reconhecimento de fala para transcrever áudios.

## Funcionalidades

- **Conversão de Áudio para Texto**: Utiliza a ferramenta whisper da OpenAI na função `speech_to_text` para transcrever áudios de manutenção em texto.
- **Geração de Checklist**: A função `generate_checklist` cria listas de verificação a partir de texto transcrito ou texto corrido.
- **Interface Gráfica com Streamlit**: Permite ao usuário fazer upload de arquivos de áudio ou inserir texto diretamente para gerar checklists.
- **Exibicao de Resultados**: Mostra os resultados numa interface interativa de facil acesso que ajuda o tecnico a se organizar quanto as tarefas e as ferramentas.

## Tecnologias Utilizadas

- Python e dotenv (para gerenciamento de variáveis de ambiente)
- OpenAI API
- Streamlit
- Feiss

## Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu_usuario/seu_repositorio.git
   cd seu_repositorio
   ```
2. Instale as dependências: É recomendado criar um ambiente virtual para instalar as dependências:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Para Linux/Mac
    venv\Scripts\activate  # Para Windows
    pip install -r requirements.txt
    ```
## Uso
1. Executar o Aplicativo Streamlit: No terminal, execute o seguinte comando:
    ```bash
    streamlit run app.py
    ```
2. Interface de Usuário:
    - Navegue até a interface de usuário que se abrirá em seu navegador.
    - Faça o upload de um arquivo de áudio (formatos suportados: OGG, MP3, WAV) ou insira um texto corrido na interface.
    - Clique no botão "Enviar Áudio" ou "Enviar Texto" para processar a entrada.
    - O resultado será exibido na área designada e também salvo em backend/prompt_result.txt.
## Estrutura do projeto
    seu_repositorio/
    │
    ├── backend/
    │   ├── checklist/
    │   │   ├── generate_checklist.py
    │   │   └── speech2text.py
    │   ├── prompt_result.txt
    │   └── ...
    ├── frontend/
    │   ├── app.py
    │   ├── maintenance_service.py
    │   ├── utils.py
    │   └── ...
    ├── requirements.txt
    └── .env

