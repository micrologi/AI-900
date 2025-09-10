from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

load_dotenv('.env')

# Configurações da sua conta no Azure
endpoint = os.getenv("endpoint")
key = os.getenv("key")

# Cria o cliente
client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Caminho do arquivo local
document_path = input('Digite o nome do documento com extensão: ')

with open(document_path, "rb") as f:
    poller = client.begin_analyze_document(
        model_id="prebuilt-invoice",   # Modelo de nota fiscal
        body=f,                        # Aquivo precisa ser passado no "body"
        content_type="application/pdf" # Tipo do arquivo (mude se for image/png, image/jpeg etc.)
    )

# Resultado
result = poller.result()

print("---- RESULTADO ----")
for doc in result.documents:
    print(f"Documento detectado com tipo: {doc.doc_type}")
    for name, field in doc.fields.items():
        print(f"{name}: {field.values} (confiança: {field.confidence})")

# Tabelas (se houver)
if result.tables:
    for table in result.tables:
        print("\nTabela detectada:")
        for cell in table.cells:
            print(f"({cell.row_index}, {cell.column_index}): {cell.content}")
else:
    print("Nenhuma tabela detectada.")