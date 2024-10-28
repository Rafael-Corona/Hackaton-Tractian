import requests

from dotenv import load_dotenv

load_dotenv()

# Defina sua chave da API do OpenAI
url = "https://api.openai.com/v1/audio/transcriptions"

def audio_para_texto(arquivo_audio):
    try:
        # Configure o cabeçalho e os dados para a requisição
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        files = {
            "file": (arquivo_audio, open(arquivo_audio, "rb")),
            "model": (None, "whisper-1")
        }
        
        # Envia a requisição
        response = requests.post(url, headers=headers, files=files)
        response.raise_for_status()  # Verifica se houve algum erro
        
        # Extrai o texto da resposta
        return response.json().get("text")
    except Exception as e:
        print("Erro ao converter áudio em texto:", e)
        return None

# Exemplo de uso
arquivo_audio = "audio_tractian.ogg"
texto_convertido = audio_para_texto(arquivo_audio)
if texto_convertido:
    print("Texto transcrito:", texto_convertido)

