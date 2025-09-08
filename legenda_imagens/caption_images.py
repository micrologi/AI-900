#pip install azure-ai-vision-imageanalysis --user
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

load_dotenv()

# Configurações da sua conta do Azure AI Foundry
endpoint = os.getenv("endpoint")
key = os.getenv("key")

# Caminho da imagem local que você quer analisar
image_path = "criancas.jpg"

# Criar cliente
client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Abrir imagem em modo binário
with open(image_path, "rb") as f:
    image_data = f.read()

# Chamar API de análise solicitando legendas (caption)
result = client.analyze(
    image_data=image_data,
    visual_features=[VisualFeatures.CAPTION]
)

# Exibir resultado
if result.caption is not None:
    print(f"Legenda: {result.caption.text} (confiança: {result.caption.confidence:.2f})")
else:
    print("Não foi possível gerar uma legenda para esta imagem.")