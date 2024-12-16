import os
import requests
from flask import Flask, jsonify
from google.cloud import storage

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    try:
        data = fetch_data()
        upload_to_gcs(str(data), os.environ["BUCKET_NAME"], "raw/traffic_data.json")
        return jsonify({"message": "Data ingestion complete!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def fetch_data():   """Obtención de los datos desde la API de tráfico."""
    url = "http://overpass-api.de/api/interpreter?data=[out:json];node[highway=traffic_signals](50.6,7.0,50.8,7.3);out;"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def upload_to_gcs(data, bucket_name, destination_blob):   """Carga de los datos a un bucket de Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_string(data, content_type="application/json")


if __name__ == "__main__":
    # Obtén el puerto desde la variable de entorno PORT o usa el puerto 8080 por defecto
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
