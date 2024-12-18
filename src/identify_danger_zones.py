from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, lit
from sklearn.cluster import KMeans
import pandas as pd
import folium
from folium.plugins import HeatMap
from google.cloud import storage

# Configura SparkSession
spark = SparkSession.builder \
    .appName("Danger Zone Prediction") \
    .getOrCreate()

def process_data(input_path):
    # Carga los datos de tráfico desde un archivo JSON
    raw_data = spark.read.json(input_path)
    
    # Explota los elementos y selecciona nodos con coordenadas válidas
    elements = raw_data.select(explode(col("elements")).alias("element"))
    nodes = elements.filter(col("element.type") == "node") \
        .select(
            col("element.id").alias("id"),
            col("element.lat").alias("latitude"),
            col("element.lon").alias("longitude"),
            col("element.tags").alias("tags")
        )
    
    return nodes

def identify_danger_zones(nodes_df):
    # Convierte los datos de Spark DataFrame a Pandas DataFrame
    nodes_pd = nodes_df.select("latitude", "longitude").toPandas()
    
    # Aplica clustering K-means para identificar densidad
    kmeans = KMeans(n_clusters=20, random_state=42)
    nodes_pd["cluster"] = kmeans.fit_predict(nodes_pd[["latitude", "longitude"]])
    
    # Calcula el tamaño de cada cluster
    cluster_sizes = nodes_pd["cluster"].value_counts().reset_index()
    cluster_sizes.columns = ["cluster", "size"]
    
    # Identifica clusters con tamaño por debajo de un umbral
    danger_threshold = cluster_sizes["size"].quantile(0.25)  # 25% más pequeños
    danger_clusters = cluster_sizes[cluster_sizes["size"] <= danger_threshold]["cluster"]
    
    # Filtra los nodos que pertenecen a zonas peligrosas
    danger_zones = nodes_pd[nodes_pd["cluster"].isin(danger_clusters)]
    
    return danger_zones, nodes_pd, kmeans.cluster_centers_

def upload_to_gcs(local_file, bucket_name, destination_blob_name):
    """ Sube un archivo local a un bucket de GCS. """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file)

def visualize_zones(danger_zones, cluster_centers, bucket_name):
    # Genera un mapa interactivo
    madrid_map = folium.Map(location=[40.4168, -3.7038], zoom_start=6)
    
    # Añade las zonas peligrosas como un mapa de calor
    HeatMap(danger_zones[["latitude", "longitude"]].values).add_to(madrid_map)
    
    # Añade los centros de los clusters
    for center in cluster_centers:
        folium.Marker(location=[center[0], center[1]], popup="Cluster Center").add_to(madrid_map)
    
    # Guarda el mapa localmente
    local_file = "danger_zones_map.html"
    madrid_map.save(local_file)
    print("Mapa guardado como 'danger_zones_map.html'")

    # Sube el archivo a GCS
    upload_to_gcs(local_file, bucket_name, "processed/danger_zones_map.html")

def main():
    # Ruta del archivo de entrada
    input_path = "gs://grupo12project/raw/traffic_data.json"
    bucket_name = "grupo12project"
    
    # Procesar datos
    nodes_df = process_data(input_path)
    
    # Identificar zonas peligrosas
    danger_zones, all_nodes, cluster_centers = identify_danger_zones(nodes_df)
    
    # Visualizar resultados y subir el mapa a GCS
    visualize_zones(danger_zones, cluster_centers, bucket_name)

if __name__ == "__main__":
    main()