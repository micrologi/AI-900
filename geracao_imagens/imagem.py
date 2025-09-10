from openai import AzureOpenAI
import requests
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import os

load_dotenv('.env')

# Configurações de ambiente
#Visão geral / OpenAI do Azure / Ponto de extremidade do OpenAI do Azure
endpoint = os.getenv("endpoint")
key = os.getenv("key")
deployment = os.getenv("deployment")

# Cliente Azure OpenAI
client = AzureOpenAI(
    api_key=key,
    api_version="2024-02-01",  
    azure_endpoint=endpoint
)

# Prompt para gerar a imagem
prompt = input('Qual imagem deseja? ("sair" para abandonar): ')

# Chamada para gerar imagem
result = client.images.generate(
    model=deployment,
    prompt=prompt,
    size="1024x1024"
)

# URL da imagem (Azure retorna link temporário)
print(result)

image_url = result.data[0].url
print(image_url)


response = requests.get(image_url)
img = Image.open(BytesIO(response.content))
img.show()
