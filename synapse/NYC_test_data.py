from azureml.opendatasets import NycTlcYellow
from pyspark.sql.functions import col

# Create a DataFrame from the Open Dataset
nyc_tlc = NycTlcYellow()
df = nyc_tlc.to_spark_dataframe()

# Select a subset of columns and data
df = df.select(
    col("tpep_pickup_datetime"),
    col("tpep_dropoff_datetime"),
    col("passenger_count"),
    col("trip_distance"),
    col("fare_amount")
).filter(col("tpep_pickup_datetime") > '2021-01-01')

# Write the DataFrame to a Synapse SQL table
df.write.mode("overwrite").saveAsTable("TestDatabase.NycTlcYellow")
