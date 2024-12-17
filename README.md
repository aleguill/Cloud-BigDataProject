1. *DESCRIPTION OF THE PROBLEM*

Urban centers face significant challenges in managing traffic flow and ensuring road safety. This project focuses on identifying high-risk urban zones based on the infrastructure of traffic signals and traffic signs across the Community of Madrid. By applying clustering algorithms (K-means) on traffic-related infrastructure data, we generate actionable insights and visualize high-risk zones on a heatmap.

2. *NEED FOR BIG DATA AND CLOUD*

- Big Data : analyzing large-scale traffic signal an sign data across Madrid generates substantial datasets, which require distributed storage and processing.
  
- Cloud : Google Cloud offers scalable storage (Cloud Storage), distributed processing (Dataproc), and automated workflows (Cloud Functions) to handle complex Big Data workloads.

- Real-time insights : cloud platforms enable efficient processing and visualization to identify traffic trends and patterns quickly.

3. *DESCRIPTION OF THE DATA*

- Source : data collected from Overpass API (OpenStreetMap), which provides geospatial data on traffic 
  signals and signs.
  
- Acquisition : queries fetch nodes and ways tagged as highway, traffic_signlas or traffic_sign within the 
  bounding box of the Community of Madrid.

- Description
    > Format : JSON format containing nested data (latitude, longitude, tags).
    > Meaning : nodes represent traffic signals and ways represent streets and road features tagged with 
      relevant metadata
    > Size : approximately 1.1 GB of raw data collected and 1.2 MB of processed data used for clustering.

4. *DESCRIPTION OF THE APPLICATION*

- Programming models and tools
    > Python : for orchestrating data ingestion, processing, and visualization.
    > PySpark (Dataproc) : to clean, process, and perform K-means clustering on large datasets.
    > Folium : to generate an interactive heatmap visualizing high-risk zones.
    > Google Cloud Platform
      | Cloud Functions : automates data ingestion into Cloud Storage.
      | Cloud Storage : stores raw and processed datasets.
      | Dataproc : performs distributed data processing and clustering.

- Platform and infrastructure
    > Cloud Storage Bucket : grupo12project
    > Dataproc Cluster
      | Workers : 2 nodes (n2-standard-4 machines).
      | Region : us-central1
    > Visualization : generated as an interactive HTML file using Folium. 

5. *SOFTWARE DESING*

- Architecture
    > Data ingestion : a Cloud Function fetches traffic signal and sign data using Overpass API and stores 
      it as JSON in Google Cloud Storage.
    > ETL Processing
      | PySpark reads raw JSON data from Cloud Storage.
      | Data is cleaned, filtered, and clustered using the K-means algorithm.
    > Visualization : Folium generates a heatmap of high-risk zones based on cluster centroids.

- Code baseline and dependencies
    > Key dependencies : google-cloud-storage, requests, pandas, folium, pyspark, sklearn.
    > Repository structure
      | Cloud Function : src/main.py
      | Spark job : src/identify_danger_zones.py
      | Visualization : processed/danger_zones_map.html

6. *USAGE*

- Instructions
    > Clone the repository
        > git clone https://github.com/aleguill/Cloud-BigDataProject.git
        > cd Cloud-BigDataProject
    > Deploy the Cloud Function to fetch and store data
        > gcloud functions deploy data_ingestion --runtime python39 \
          --trigger-http --allow-unauthenticated --region=us-central1 \
          --source=src --entry-point main --set-env-vars BUCKET_NAME=grupo12project
    > Create the Dataproc cluster
        > gcloud compute networks subnets update default --region=europe-southwest1 \
          --enable-private-ip-google-access
        > gcloud dataproc clusters create traffic-cluster --region=us-central1 \
          --master-machine-type=n2-standard-4 --master-boot-disk-size=50 \
          --worker-machine-type=n2-standard-4 --worker-boot-disk-size=50 \
          --enable-component-gateway
    > Submit the Spark job to process data and generate clusters
        > gcloud dataproc jobs submit pyspark --cluster traffic-cluster \
          --region=us-central1 src/identify_danger_zones.py

    > - Output : interactive map saved as danger_zones_map.html

7. *PERFORMANCE EVALUATION*

- Scalability tests
    > Run of Spark jobs with varyig node counts (e.g. 2,4,6)
    > Measurement of  execution times and analysis of speedup
      | 2 workers : ~30 seconds
      | 4 workers : ~29 seconds
      | 6 workers : ~28 seconds
    > Speedup : not so different between each other (values near 1)
      | 4 workers : 30/29 = 1.034
      | 6 workers : 30/28 = 1.071

- Optimization effort : K-means clustering was tuned to identify the optimal number of clusters (k = 20).

8. *ADVANCED FEATURES*

- K-means clustering
    > Traffic data is clustered to identify high-risk zones.
    > Cluster centroids highlight areas with dense traffic infrastructure.

- Interactive heatmaps : Folium maps provide zoomable, detailed views of high-risk areas. 

9. *CONCLUSIONS*

- Goals achieved
    > Successfully identified high-risk urban zones in Madrid based on traffic infrastructure.
    > Generated an interactive heatmap for actionable insights.
    > Opmitmized data processing using Google Cloud and PySpark.

- Improvements suggested : explore real-time streaming pipelines using Dataflow.

- Lessons learned 
    > Determining the optimal number of clusters requieres careful tuning.
    > Processing nested JSON data efficiently is key to performance.

- Future work
    > Incorporate live traffic data for real-time risk analysis.
    > Use advanced machine learning models to predict traffic patterns and risks.

10. *REFERENCES*

- Overpass API documentation : "https://overpass-api.de/"

- OpenStreetMap API documentation : "https://wiki.openstreetmap.org/wiki/Overpass_API"

- Google Cloud documentation : "https://cloud.google.com/docs?hl=es-419"

- Apache Spark documentation : "https://spark.apache.org/docs/3.5.3/api/python/getting_started/index.html"

- Scikit-learn clustering guide : "https://qu4nt.github.io/sklearn-doc-es/modules/clustering.html#k-means"

- Folium Library Documentation : "https://python-visualization.github.io/folium/latest/"
