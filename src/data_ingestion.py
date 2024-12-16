import os
import requests
from google.cloud import storage

def fetch_data():
  url = "http://overpass-api.de/api/interpreter?data=[out:json];node[highway=traffic_signals](50.6,7.0,50.8,7.3);out;"
  response = requests.get(url)
  response.raise_for_status()
  return response.json()

def upload_to_gcs(data, bucket_name, destination_blob):
  storage_client = storage.Client()
  bucket = storage_client.bucket(bucket_name)
  blob = bucket.blob(destination_blob)
  blob.upload_from_string(data, content_type = "application/json")

def main(request):
  data = fetch_data()
  upload_to_gcs(str(data), os.environ['BUCKET_NAME'], "raw/traffic_data.json")
  return "Data ingestion complete"
