from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression

def main():
  spark = SparkSession.builder.appName("ETL and ML Job").getOrCreate()

  # Load raw data from Cloud Storage
  raw_data = spark.read.json("gs://your-bucket-name/raw/traffic_data.json")    #CA,BIAR BUCKET NAME

  # Transform data
  clean_data = raw_data.select("id", "lat", "lon", "tags", "timestamp").filter(raw_data-tags.isNotNull())

  # Feature engineering for ML
  assembler = VectorAssembler(inputCols = ["lat", "lon"], outputCol = "features")
  ml_data = assembler.transform(clean_data)

  # Train a regression model to predict congestion
  lr = LinearRegression(featuresCol = "features", labelCol = "timestamp")
  lr_model = lr.fit(ml_data)

  # Save model to Cloud Storage
  model_path = "gs://your-bucket-name/models/traffic_congestion_model"   #CAMBIAR BUCKET NAME
  lr_model.write().overwrite().save(model_path)

  # Write processed data back to Cloud Storage
  clean_data.write.csv("gs://your-bucket-name/processed/cleaned_data.csv", header = True)   #CAMBIAR BUCKET NAME

  spark.stop()

if __name__ == "__main__":
  main()
