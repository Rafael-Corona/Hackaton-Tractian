from openai import OpenAI
from dotenv import load_dotenv
from checklist.generate_checklist import generate_checklist
from checklist.speech2text import speech_to_text

load_dotenv()
client = OpenAI()
audio = 'data/audio/audio_wpp.ogg'

t = speech_to_text(client, audio)
c = generate_checklist(client, t)
print(c)
