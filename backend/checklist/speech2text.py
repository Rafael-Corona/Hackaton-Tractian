from openai import OpenAI

def speech_to_text(client: OpenAI, audio_filename: str) -> str:
    audio_file= open(audio_filename, "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file
    )
    
    return transcription.text