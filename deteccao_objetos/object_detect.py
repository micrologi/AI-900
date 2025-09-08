#pip install azure-ai-vision-imageanalysis --user
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

load_dotenv('.env')

endpoint =  os.getenv("endpoint")
api_key =  os.getenv("key")

client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

def detect_objects_local(image_path: str):
    with open(image_path, "rb") as f:
        image_data = f.read()

    result = client.analyze(
        image_data=image_data,
        visual_features=[VisualFeatures.OBJECTS]
    )

    objnum = 1
    if result.objects:
        for obj in result.objects['values']:
            print(f"=========== Objeto {objnum} ===========")
            print(f"Objeto: {obj['tags'][0]['name']}")
            print(f"Confidence: {obj['tags'][0]['confidence']}")
            print(f"Quadrante (boundingBox): {obj['boundingBox']}")
            print("")
            objnum += 1
    else:
        print("Nenhum objeto detectado.")

if __name__ == "__main__":
    detect_objects_local("objetos.jpg")
