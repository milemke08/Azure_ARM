# Import necessary libraries
from pyspark.sql import SparkSession
from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import DataLakeServiceClient
import os

# Initialize Spark session
spark = SparkSession.builder.appName("AzureDataLakeTransformations").getOrCreate()

# Define Azure Data Lake credentials
tenant_id = "<your-tenant-id>"
client_id = "<your-client-id>"
client_secret = "<your-client-secret>"
storage_account_name = "<your-storage-name>"
storage_account_key = "<your-storage-key>"
container_name = "<your-container-name>"

spark.conf.set("fs.azure.account.key.{}.dfs.core.windows.net".format(storage_account_name), storage_account_key)
# Initialize ClientSecretCredential
credential = ClientSecretCredential(tenant_id, client_id, client_secret)

# Initialize DataLakeServiceClient
service_client = DataLakeServiceClient(account_url=f"https://{storage_account_name}.dfs.core.windows.net", credential=credential)

# Function to read data from Azure Data Lake
def read_data_from_adls(path):
    print(f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/{path}")
    try:
        df = spark.read.csv(f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/{path}", header=True, inferSchema=True)
        return df
    except Exception as e:
        print(f"Error reading data: {e}")

# Function to perform basic data transformations
def transform_data(df):
    try:
        df_transformed = df.withColumnRenamed("Day", "Day Number")  # Example transformation
        return df_transformed
    except Exception as e:
        print(f"Error transforming data: {e}")

# Function to write data back to Azure Data Lake
def write_data_to_adls(df, path):
    try:
        df.write.csv(f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/{path}", mode="overwrite", header=True)
    except Exception as e:
        print(f"Error writing data: {e}")

# Main workflow
if __name__ == "__main__":
    input_path = "Azure_SDK_Learning.csv"
    output_path = "Azure_SDK_Learning_output.csv"
    
    df = read_data_from_adls(input_path)
    if df:
        df_transformed = transform_data(df)
        if df_transformed:
            write_data_to_adls(df_transformed, output_path)
