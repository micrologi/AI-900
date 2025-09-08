#pip install azure-ai-documentintelligence --user
from typing import Optional
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, AnalyzeResult
from dotenv import load_dotenv
import os

load_dotenv('.env')

# Pegue as credenciais do ambiente (recomendado)
ENDPOINT = os.getenv("endpoint")
KEY = os.getenv("key")

client = DocumentIntelligenceClient(endpoint=ENDPOINT, credential=AzureKeyCredential(KEY))

def ocr_from_file(path: str) -> AnalyzeResult:
    """
    Executa OCR em um arquivo local usando o modelo prebuilt-read.
    Aceita PDFs, imagens (JPG/PNG/TIFF), etc.
    """
    with open(path, "rb") as f:
        poller = client.begin_analyze_document(
            model_id="prebuilt-read",
            body=f,  # envio do arquivo binário
        )
    return poller.result()

def ocr_from_url(url: str) -> AnalyzeResult:
    """
    Executa OCR em um arquivo disponível por URL pública.
    """
    request = AnalyzeDocumentRequest(url_source=url)
    poller = client.begin_analyze_document(
        model_id="prebuilt-read",
        analyze_request=request,
    )
    return poller.result()

def print_text(result: AnalyzeResult) -> None:
    """
    Imprime o texto por página (linhas) e, ao final, o texto por parágrafos.
    """
    for page in result.pages or []:
        print(f"\n=== Página {page.page_number} ===")
        for line in (page.lines or []):
            print(line.content)

    # Se quiser um "texto corrido", os parágrafos já vêm em ordem lógica
    '''
    if result.paragraphs:
        print("\n=== Texto por parágrafos ===")
        for p in result.paragraphs:
            print(p.content)
    '''

if __name__ == "__main__":
    resultado = ocr_from_file("carta2.jpeg")
    print_text(resultado)
