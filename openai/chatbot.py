from openai import AzureOpenAI
from dotenv import load_dotenv
import os

load_dotenv('.env')

endpoint = os.getenv("endpoint")
subscription_key = os.getenv("key")
model_name = os.getenv('model_name')
deployment = os.getenv('deployment_chatbot')
api_version = os.getenv('api_version')

client = AzureOpenAI(
    api_version=api_version,
    azure_endpoint=endpoint,
    api_key=subscription_key,
)

while True:
    pergunta = input("\033[1;33m:> ")

    if pergunta.lower() == 'sair':
        print('\033[1;97mBye, bye...')
        break

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "você é um especialista de assuntos gerais.",
            },
            {
                "role": "user",
                "content": f"responda-me em 1 frase: {pergunta}",
            }
        ],
        max_tokens=4096,
        temperature=1.0,
        top_p=1.0,
        model=deployment
    )

    print('\033[1;97m' + response.choices[0].message.content)