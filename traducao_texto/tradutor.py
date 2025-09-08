#pip install requests uuid --user
import requests, uuid, json
from dotenv import load_dotenv
import os

load_dotenv('.env')

endpoint = os.getenv("endpoint")
resource_key = os.getenv("key")
region = os.getenv('region')

while True:

    texto = input('Texto em português: ')
    
    if texto.lower() == 'sair':
        print('Bye, bye...')
        break

    path = '?api-version=3.0'
    params = '&from=pt-br&to=en'
    constructed_url = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': resource_key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text' : texto
    }]

    request = requests.post(constructed_url, headers=headers, json=body)

    response = request.json()
    print(response[0]['translations'][0]['text'])