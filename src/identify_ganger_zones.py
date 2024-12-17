from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, lit
from sklearn.cluster import KMeans
import pandas as pd
import folium
from folium.plugins import HeatMap
from google.cloud import storage

spark = SparkSession.builder \
    .appName("Danger Zone Prediction") \
    .getOrCreate()

def process_data(input_path):
    raw_data = spark.read.json(input_path)
    
    # Elements explosion and valid nodes filtering
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
    # Spark DataFrame => Pandas DataFrame
    nodes_pd = nodes_df.select("latitude", "longitude").toPandas()
    
    # K-means clustering for density identifying
    kmeans = KMeans(n_clusters=20, random_state=42)
    nodes_pd["cluster"] = kmeans.fit_predict(nodes_pd[["latitude", "longitude"]])
    
    # Calculates each cluster's size
    cluster_sizes = nodes_pd["cluster"].value_counts().reset_index()
    cluster_sizes.columns = ["cluster", "size"]
    
    # Identifies clusters below a minimum
    danger_threshold = cluster_sizes["size"].quantile(0.25)  # 25% smaller
    danger_clusters = cluster_sizes[cluster_sizes["size"] <= danger_threshold]["cluster"]
    
    # Filters nodes that are in a high-risk area
    danger_zones = nodes_pd[nodes_pd["cluster"].isin(danger_clusters)]
    
    return danger_zones, nodes_pd, kmeans.cluster_centers_

def upload_to_gcs(local_file, bucket_name, destination_blob_name):
    """ File upload to GCS """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(local_file)

def visualize_zones(danger_zones, cluster_centers, bucket_name):
    # Generates an interactive map
    madrid_map = folium.Map(location=[40.4168, -3.7038], zoom_start=6)
    
    # Adds high-risk areas as a heatmap
    HeatMap(danger_zones[["latitude", "longitude"]].values).add_to(madrid_map)
    
    # Adds clusters' centers
    for center in cluster_centers:
        folium.Marker(location=[center[0], center[1]], popup="Cluster Center").add_to(madrid_map)
    
    # Saves the map locally
    local_file = "danger_zones_map.html"
    madrid_map.save(local_file)
    print("Mapa guardado como 'danger_zones_map.html'")

    # File upload to GCS
    upload_to_gcs(local_file, bucket_name, "processed/danger_zones_map.html")

def main():
    # Input file path
    input_path = "gs://grupo12project/raw/traffic_data.json"
    bucket_name = "grupo12project"
    
    # Data processing
    nodes_df = process_data(input_path)
    
    # High-risk zones identification
    danger_zones, all_nodes, cluster_centers = identify_danger_zones(nodes_df)
    
    # Results visualization and upload to GCS
    visualize_zones(danger_zones, cluster_centers, bucket_name)

if __name__ == "__main__":
    main()
