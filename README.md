1. *DESCRIPTION OF THE PROBLEM*

The project focuses on analyzing real-time traffic patterns and predicting congestion using Big Data tools on Google Cloud. This problem is highly relevant for urban planning and reducing commute times, leveraging scalable data analysis capabilities of cloud platforms.

2. *NEED FOR BIG DATA AND CLOUD*

- Big Data : the traffic dataset contains GPS locations, timestamps, and vehicle densities exceeding 1 GB, 
  representing high volume and velocity. Challenges include managing structured and unstructured data and 
  processing it in near real-time.
  
- Google Cloud : Google Cloud services like Dataproc and BigQuery enable scalable data and processing 
  processing and SQL-based analytics. Cloud Functions facilitate event-driven architectures for dynamic 
  data pipelines.

3. *DESCRIPTION OF THE DATA*

- Source : data collected from OpenStreetMap.
  
- Acquisition : usage of the OpenStreetMap API for downloading traffic and geographic data. This is done 
  using Python library osmnx.

- Description
    > Attributes : latitude, longitude, timestamps, speed, and congestion levels.
    > Format : JSON and CSV.
    > Size : approximately 1.5 GB of raw data collected over a week.

4. *DESCRIPTION OF THE APPLICATION*

- Architecture : Data is ingested via API. processed in Google Cloud Dataproc (Spark), stored in BigQuery, 
  and visualized using Google Data Studio. Architecture diagram includes:
    > Data ingestion : Python scripts running on Cloud Functions.
    > Processing : Dataproc Spark jobs for ETL (Extract, Transform, Load).
    > Storage : BigQuery for SQL-based queries.
    > Visualization : Google Data Studio for traffic trends.

- Programming models : Spark and Python for distributed processing.

- Platforms : Google Cloud services such as Cloud Storage, Dataproc, BigQuery, and Cloud Functions.

5. *SOFTWARE DESING*

- Architecture : data ingestion -> ETL (Dataproc) -> Storage (BigQuery) -> Visualization (Data Studio).

- Code baseline : Python and Pyspark for data processing.

- Dependencies
    > Python : requests, pandas, google-cloud-bigquery, osmnx.
    > Spark : Pyspark.

- Data Flow
    > Real-time data ingested and temporarily stored in Cloud Storage.
    > ETL pipeline processes data in batches, loading clean data into BigQuery.

6. *USAGE*

- Instructions
    > Clone the repository
        git clone https://github.com/aleguill/Cloud-BigDataProject.git
        cd Cloud-BigDataProject
    > Install dependencies
        pip install -r requierements.txt
    > Run data ingestion
        python src/data_ingestion.py --output gs://bucket-name/raw-data
    > Submit Dataproc job
        gcloud dataproc jobs submit pyspark src/etl_job.py --cluster=my-cluster --region=us-central1
    > Query BigQuery data
        SELECT * FROM `project-id.dataset-id.table-name` LIMIT 10;

- Output : cleaned traffic data and visualizations of congestion trends.

7. *PERFORMANCE EVALUATION*

- Scalability tests
    > "Run Spark jobs with varyig node counts (e.g., 2,4,8)"
    > "Measure execution times and analyze speedup"

- Optimization efforts
    > "Enable caching for repeated quieries in BigQuery"
    > "Optimize Spark partitions for balanced workloads"

- Overheads
    > "Data transfer latency and job scheduling delays identified as bottlenecks"

- Results
    > "Charted improvements showing linear scalability up to 8 nodes"

8. *ADVANCED FEATURES*

- Machine Learning
    > "Implement traffic pattern prediction using Spark MLlib"
    > "Train refression models to forecast congestion levels"

- Optimization techniques
    > "Use of custom partitioners for Spark jobs"
    > "Efficient use of Google Cloud Preemptible VMs to reduce costs"

9. *CONCLUSIONS*

- Goals achieved
    > Successfull ingested, processed, and visualized traffic data.
    > Demonstrated scalability and cost-effectiveness using Google Cloud.

- Improvements suggested : explore real-time streaming pipelines using Dataflow.

- Lessons learned : cloud-native tools simplify distributed processing but require careful cost management.

- Future work : incorporate additional data sources (e.g., weather).

10. *REFERENCES*

- "OpenStreetMap API documentation"

- "Google Cloud Dataproc and BigQuery documentation"

- "Research papers on traffic congestion analysis"

- "Python library documentation for osmnx"
