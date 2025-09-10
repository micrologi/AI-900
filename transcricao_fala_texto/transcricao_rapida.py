import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os

load_dotenv('.env')

speech_key = os.getenv("key")
region = os.getenv('region')  

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
speech_config.speech_recognition_language = "pt-BR"

recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

print("Fale algo no microfone...")
result = recognizer.recognize_once()

if 'sair' in result.text.lower():
    os.system("shutdown /s /t 0")

print("Resultado:", result.text)
