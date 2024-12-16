import os
import requests
from google.cloud import storage

def fetch_data():
    """Obtén datos desde la API de tráfico para toda España."""
    url = "http://overpass-api.de/api/interpreter?data=[out:json];node[highway=traffic_signals](40.0,-4.5,41.0,-3.0);out;"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def upload_to_gcs(data, bucket_name, destination_blob):
    """Sube datos a un bucket de Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_string(data, content_type="application/json")

def main(request):
    """Función principal para Google Cloud Functions."""
    try:
        # Obtén los datos de la API
        data = fetch_data()

        # Nombre del bucket
        bucket_name = os.environ.get("BUCKET_NAME", "grupo12project")
        
        # Sube los datos al bucket con un nombre específico
        upload_to_gcs(str(data), bucket_name, "raw/traffic_data.json")

        # Respuesta de éxito
        return {"message": "Data ingestion complete"}, 200
    except Exception as e:
        # Manejo de errores
        return {"error": str(e)}, 500
