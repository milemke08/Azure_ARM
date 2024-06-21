import os
from azureml.opendatasets import NycTlcYellow
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from dotenv import load_dotenv
import pyodbc

# Load environment variables
load_dotenv()

# Set up Azure Synapse connection details
synapse_server = f"{os.getenv('AZURE_SYNAPSE_WORKSPACE')}.sql.azuresynapse.net"
database = os.getenv('AZURE_SYNAPSE_SQL_POOL')
username = os.getenv('AZURE_SQL_ADMIN')
password = os.getenv('AZURE_SQL_PASSWORD')
driver = "{ODBC Driver 17 for SQL Server}"

# Initialize Spark session
spark = SparkSession.builder \
    .appName("NYC_TLC_Yellow_Data") \
    .getOrCreate()

# Load NYC TLC Yellow data using Azure Open Datasets
nyc_tlc = NycTlcYellow()
df = nyc_tlc.to_spark_dataframe()

# Select a subset of columns and filter data
df = df.select(
    col("tpep_pickup_datetime"),
    col("tpep_dropoff_datetime"),
    col("passenger_count"),
    col("trip_distance"),
    col("fare_amount")
).filter(col("tpep_pickup_datetime") > '2021-01-01')

# Write the DataFrame to a Synapse SQL table
jdbc_url = f"jdbc:sqlserver://{synapse_server}:1433;database={database};user={username};password={password};encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.sql.azuresynapse.net;loginTimeout=30;"

df.write \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", "NYCTLCYellowData") \
    .option("driver", "com.microsoft.sqlserver.jdbc.SQLServerDriver") \
    .mode("overwrite") \
    .save()

print("Data successfully written to Azure Synapse.")
