from azure.identity import DefaultAzureCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import Factory
from azure.mgmt.datafactory.models import *
from azure.mgmt.storage import StorageManagementClient
import os
import json
from dotenv import load_dotenv

#use this to create linked service and connection to yellow taxi data: https://learn.microsoft.com/en-us/azure/open-datasets/dataset-taxi-yellow?tabs=pyspark
#first stage the data in blob storage, then load into sql

def create_data_factory(subscription_id, resource_group_name, data_factory_name, location):
    try:
        # Set up Azure credentials and clients
        credential = DefaultAzureCredential()
        adf_client = DataFactoryManagementClient(credential, subscription_id)

        # Create the Data Factory
        factory = Factory(location=location)
        adf_client.factories.create_or_update(resource_group_name, data_factory_name, factory)

        print(f"Data Factory '{data_factory_name}' created successfully in resource group '{resource_group_name}'.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def create_blob_storage_linked_service(subscription_id, resource_group_name, data_factory_name, linked_service_name, storage_account_name, storage_account_key):
    try:
        # Set up Azure credentials and clients
        credential = DefaultAzureCredential()
        adf_client = DataFactoryManagementClient(credential, subscription_id)

        # Create a linked service to Azure Blob Storage
        if storage_account_key != 0:
            linked_service = LinkedServiceResource(properties=AzureBlobStorageLinkedService(
                connection_string=f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"))
        else:
            # C:\Users\zdoi\Documents\Python\Azure\AzureSDK\Azure_SDK\data factory\6 import_with_azdf.py
            with open(r'data factory\yellow_taxi_linked_service_config.json', 'r') as json_file:
                linked_service_config = json.load(json_file)
            linked_service = LinkedServiceResource(properties=linked_service_config['properties'])
            # linked_service = LinkedServiceResource(properties=AzureBlobStorageLinkedService(
            #     connection_string="BlobEndpoint=https://azureopendatastorage.blob.core.windows.net/nyctlc"))
            
        adf_client.linked_services.create_or_update(resource_group_name, data_factory_name, linked_service_name, linked_service)

        print(f"Linked service '{linked_service_name}' created successfully in Data Factory '{data_factory_name}'.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def create_sql_db_linked_service(subscription_id, resource_group_name, data_factory_name, linked_service_name, sql_server_name, db_name, user, password):
    try:
        
        # Set up Azure credentials and clients
        credential = DefaultAzureCredential()
        adf_client = DataFactoryManagementClient(credential, subscription_id)

        with open(r'data factory\sql_server_linked_service_config.json', 'r') as json_file:
                linked_service_config = json.load(json_file)
        linked_service = LinkedServiceResource(properties=linked_service_config['properties'])
        # Create a linked service to Azure Blob Storage
        # linked_service = LinkedServiceResource(properties=AzureSqlDatabaseLinkedService(
        #     # connection_string=f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"
        #     connection_string=f"Server=tcp:{sql_server_name}.database.windows.net,1433;Initial Catalog={db_name};User ID={user};Password={password};Encrypt=true;Connection Timeout=30;"
        # ))
        adf_client.linked_services.create_or_update(resource_group_name, data_factory_name, linked_service_name, linked_service)

        print(f"Linked service '{linked_service_name}' created successfully in Data Factory '{data_factory_name}'.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def create_datasets(subscription_id, resource_group_name, data_factory_name, blob_linked_service_name, sql_linked_service_name):
    try:
        # Set up Azure credentials and clients
        credential = DefaultAzureCredential()
        adf_client = DataFactoryManagementClient(credential, subscription_id)

        blob_dataset = DatasetResource(properties=AzureBlobDataset(
            linked_service_name=LinkedServiceReference(reference_name=blob_linked_service_name, type='LinkedServiceReference'),
            folder_path='nyctlc/yellow/puYear=2019/puMonth=12',
            format=TextFormat(column_delimiter=',')
        ))

        yt_blob_dataset = DatasetResource(properties=AzureBlobDataset(
            linked_service_name=LinkedServiceReference(reference_name="YellowTaxiLS", type='LinkedServiceReference'),
            folder_path='nyctlc/yellow/puYear=2019/puMonth=12',
            format=TextFormat(column_delimiter=',')
        ))

        parquet_dataset = DatasetResource(properties=ParquetDataset(
            linked_service_name=LinkedServiceReference(reference_name=blob_linked_service_name),
            folder_path='nyctlc',
            file_name='yellow/puYear=2019/puMonth=12/part-00004-tid-8898858832658823408-a1de80bd-eed3-4d11-b9d4-fa74bfbd47bc-426331-133.c000.snappy.parquet'
))

        sql_dataset = DatasetResource(properties=AzureSqlTableDataset(
            linked_service_name=LinkedServiceReference(reference_name=sql_linked_service_name, type='LinkedServiceReference'),
            table_name='YellowTaxiData'
        ))

        adf_client.datasets.create_or_update(resource_group_name, data_factory_name, 'BlobDataset', blob_dataset)
        print(f"dataset created successfully in Data Factory '{data_factory_name}'.")
        adf_client.datasets.create_or_update(resource_group_name, data_factory_name, 'SqlDataset', sql_dataset)
        print(f"dataset created successfully in Data Factory '{data_factory_name}'.")
        adf_client.datasets.create_or_update(resource_group_name, data_factory_name, 'BlobDatasetYT', yt_blob_dataset)
        print(f"dataset created successfully in Data Factory '{data_factory_name}'.")
        adf_client.datasets.create_or_update(resource_group_name, data_factory_name, 'ParquetDataset', parquet_dataset)
        print(f"dataset created successfully in Data Factory '{data_factory_name}'.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def create_data_factory_pipeline(subscription_id, resource_group_name, data_factory_name):
    try:
        # Set up Azure credentials and clients
        credential = DefaultAzureCredential()
        adf_client = DataFactoryManagementClient(credential, subscription_id)

        # # Define the linked services
        # linked_service_blob = LinkedServiceReference(reference_name=blob_storage_linked_service, type='LinkedServiceReference')
        # linked_service_adls = LinkedServiceReference(reference_name=data_lake_linked_service, type='LinkedServiceReference')

        # # Define the source dataset
        # blob_storage_dataset = DatasetResource(properties=AzureBlobDataset(
        #     linked_service_name=linked_service_blob,
        #     folder_path=blob_container,
        #     file_name=blob_path
        # ))

        # # Define the sink dataset
        # adls_dataset = DatasetResource(properties=AzureDataLakeStoreDataset(
        #     linked_service_name=linked_service_adls,
        #     folder_path=f"{data_lake_file_system}/{data_lake_directory}",
        #     file_name=blob_path.split('/')[-1]  # Assuming you want to keep the same file name
        # ))

        # # Create datasets in the Data Factory
        # adf_client.datasets.create_or_update(resource_group_name, data_factory_name, 'BlobStorageDataset', blob_storage_dataset)
        # adf_client.datasets.create_or_update(resource_group_name, data_factory_name, 'DataLakeStorageDataset', adls_dataset)

        # Create the Copy Activity - Blob to blob
        copy_activity_blob_to_blob = CopyActivity(
            name='CopyBlobToSqlYellowTaxi',
            inputs=[DatasetReference(reference_name='BlobDatasetYT', type='DatasetReference')],
            outputs=[DatasetReference(reference_name='BlobDataset', type='DatasetReference')],
            source=BlobSource(),
            sink=BlobSink()
        )

        # Create the Copy Activity - Blob to SQL
        copy_activity_blob_to_sql = CopyActivity(
            name='CopySqlYellowTaxiBlobtoSQL',
            inputs=[DatasetReference(reference_name='BlobDataset', type='DatasetReference')],
            outputs=[DatasetReference(reference_name='SqlDataset', type='DatasetReference')],
            source=ParquetSource(),
            sink=SqlSink()
        )

        # Create the pipeline with the Copy Activity
        pipeline_name = 'BlobToDataLakePipeline'
        pipeline = PipelineResource(activities=[copy_activity_blob_to_blob,copy_activity_blob_to_sql])
        adf_client.pipelines.create_or_update(resource_group_name, data_factory_name, pipeline_name, pipeline)

        print(f"Pipeline '{pipeline_name}' created successfully!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def run_pipeline(resource_group_name, data_factory_name, pipeline_name):
    # Set up Azure credentials and clients
    credential = DefaultAzureCredential()
    adf_client = DataFactoryManagementClient(credential, subscription_id)
    # Trigger the pipeline run
    run_response = adf_client.pipelines.create_run(resource_group_name, data_factory_name, pipeline_name)
    print(f"Pipeline run triggered successfully with run ID: {run_response.run_id}")

if __name__ == "__main__":
    load_dotenv()

    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')  # Replace with your Azure subscription ID 
    resource_group_name = os.getenv('RESOURCE_GROUP_NAME')  # Replace with your resource group name
    data_factory_name = os.getenv('DATA_FACTORY_NAME')  # Replace with your Data Factory name
    location = os.getenv('LOCATION')  # Replace with your location, e.g., 'eastus'
    
    data_lake_linked_service  = os.getenv('DATA_LAKE_LINKED_SERVICE')  # Replace with your linked service name
    storage_account_name = os.getenv('STORAGE_ACCOUNT_NAME') # Replace with your storage account name
    storage_account_key = os.getenv('STORAGE_ACCOUNT_KEY')  # Replace with your storage account key

    blob_storage_linked_service_name = os.getenv('DATA_LAKE_LINKED_SERVICE')  # Replace with your linked service name
    blob_storage_account_name = os.getenv('BLOB_STORAGE_ACCOUNT_NAME')  # Replace with your storage account name
    blob_storage_account_key = os.getenv('BLOB_STORAGE_ACCOUNT_KEY')  # Replace with your storage account key

    sql_server = os.getenv('SQL_SERVER_NAME') 
    sql_db = os.getenv('SQL_DATABASE_NAME') 
    sql_user = os.getenv('ADMIN_USER') 
    sql_password = os.getenv('ADMIN_PASSWORD') 
    sql_linked_service_name = os.getenv('SQL_LINKED_SERVICE')

    # blob_container = os.getenv('BLOB_CONTAINER')  # Replace with your Blob container name
    # blob_path = os.getenv('BLOB_PATH')  # Replace with your Blob file path
    # data_lake_file_system = os.getenv('DATA_LAKE_FILE_SYSTEM')  # Replace with your Data Lake file system name
    # data_lake_directory = os.getenv('DATA_LAKE_DIRECTORY')  # Replace with your Data Lake directory

    create_data_factory(subscription_id, resource_group_name, data_factory_name, location)

    create_blob_storage_linked_service(subscription_id, resource_group_name, data_factory_name, data_lake_linked_service , storage_account_name, storage_account_key)

    create_blob_storage_linked_service(subscription_id, resource_group_name, data_factory_name, "YellowTaxiLS" , storage_account_name, 0)
    
    create_sql_db_linked_service(subscription_id, resource_group_name, data_factory_name, sql_linked_service_name, sql_server, sql_db, sql_user, sql_password)

    create_datasets(subscription_id, resource_group_name, data_factory_name, blob_storage_linked_service_name, sql_linked_service_name)

    create_data_factory_pipeline(subscription_id, resource_group_name, data_factory_name)

    run_pipeline(resource_group_name,data_factory_name,'BlobToDataLakePipeline')
