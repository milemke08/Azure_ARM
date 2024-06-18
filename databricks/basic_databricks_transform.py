# Import necessary libraries
from pyspark.sql import SparkSession
from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import DataLakeServiceClient
import os

# Initialize Spark session
spark = SparkSession.builder.appName("AzureDataLakeTransformations").getOrCreate()

# Define Azure Data Lake credentials
tenant_id = os.getenv('TENANT_ID')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
storage_account_name = "mystrgeactazsdk2adlsv2"
container_name = "databricks-container-dev"

# Initialize ClientSecretCredential
credential = ClientSecretCredential(tenant_id, client_id, client_secret)

# Initialize DataLakeServiceClient
service_client = DataLakeServiceClient(account_url=f"https://{storage_account_name}.dfs.core.windows.net", credential=credential)

# Function to read data from Azure Data Lake
def read_data_from_adls(path):
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
