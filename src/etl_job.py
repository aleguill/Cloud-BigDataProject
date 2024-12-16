from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression

def main():
  spark = SparkSession.builder.appName("ETL and ML Job").getOrCreate()

  # Load raw data from Cloud Storage
  raw_data = spark.read.json("gs://grupo12project/raw/traffic_data.json")

  # Transform data
  clean_data = raw_data.select("id", "lat", "lon", "tags", "timestamp").filter(raw_data-tags.isNotNull())

  # Feature engineering for ML
  assembler = VectorAssembler(inputCols = ["lat", "lon"], outputCol = "features")
  ml_data = assembler.transform(clean_data)

  # Train a regression model to predict congestion
  lr = LinearRegression(featuresCol = "features", labelCol = "timestamp")
  lr_model = lr.fit(ml_data)

  # Save model to Cloud Storage
  model_path = "gs://grupo12project/models/traffic_congestion_model"
  lr_model.write().overwrite().save(model_path)

  # Write processed data back to Cloud Storage
  clean_data.write.csv("gs://grupo12project/processed/cleaned_data.csv", header = True)

  spark.stop()

if __name__ == "__main__":
  main()
