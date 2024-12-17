import os
import requests
from google.cloud import storage

def fetch_data():
    """Obtención de los datos desde la API de tráfico."""
    url = "http://overpass-api.de/api/interpreter?data=[out:json];node[highway=traffic_signals](40.10,-4.50,41.10,-3.20);out;"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def upload_to_gcs(data, bucket_name, destination_blob):
    """Carga de los datos a un bucket de Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_string(data, content_type="application/json")

def main(request):
    """Función principal para Google Cloud Functions."""
    try:
        data = fetch_data()
        bucket_name = "grupo12project"
        upload_to_gcs(str(data), bucket_name, "raw/traffic_data.json")
      
        return {"message": "Data ingestion complete"}, 200
    except Exception as e:
        return {"error": str(e)}, 500
