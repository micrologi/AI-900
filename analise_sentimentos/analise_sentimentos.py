# pip install python-dotenv
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os 

load_dotenv() 

while True:
    opiniao = input("Informe sua opinião: ")
    
    if opiniao.lower() == 'sair':
        print('Bye, bye...')
        break

    endpoint = os.getenv("endpoint")
    key = os.getenv("key")

    # Autenticação
    credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

    # Textos para análise (em português)
    documentos = [opiniao]

    # Chamando a API de análise de sentimentos
    response = client.analyze_sentiment(documents=documentos, language="pt")

    # Exibindo resultados
    for idx, doc in enumerate(response):
        if not doc.is_error:
            print(f"Texto: {documentos[idx]}")
            print(f"Sentimento geral: {doc.sentiment}")
            print(f"Confiança -> Positivo: {doc.confidence_scores.positive:.2f}, "
                f"Neutro: {doc.confidence_scores.neutral:.2f}, "
                f"Negativo: {doc.confidence_scores.negative:.2f}\n")
        else:
            print(f"Erro no documento {idx}: {doc.error}")
