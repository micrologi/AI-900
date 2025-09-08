import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os

load_dotenv('.env')

speech_key = os.getenv("key")
region = os.getenv('region')

speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
speech_config.speech_recognition_language = "pt-BR"

recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)


numeros = { 'um': 1,
            'dois':2,
            'três':3,
            'quatro':4,
            'cinco':5}
valores = []
contador = 0
while True:
    print("Valor (ou Sair)")
    result = recognizer.recognize_once()
    print("Resultado:", result.text.lower()[:-1])

    if result.text.lower() == 'sair':
        break
    
    valores.append(numeros[result.text.lower()[:-1]])
    
#os.system("shutdown /s /t 0")