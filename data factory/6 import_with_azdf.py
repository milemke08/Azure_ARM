from azure.identity import DefaultAzureCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import Factory
from azure.mgmt.datafactory.models import *
from azure.mgmt.storage import StorageManagementClient

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
        linked_service = LinkedServiceResource(properties=AzureBlobStorageLinkedService(
            connection_string=f"DefaultEndpointsProtocol=https;AccountName={storage_account_name};AccountKey={storage_account_key};EndpointSuffix=core.windows.net"
        ))
        adf_client.linked_services.create_or_update(resource_group_name, data_factory_name, linked_service_name, linked_service)

        print(f"Linked service '{linked_service_name}' created successfully in Data Factory '{data_factory_name}'.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")


def create_data_factory_pipeline(subscription_id, resource_group_name, data_factory_name, blob_storage_linked_service, data_lake_linked_service, blob_container, blob_path, data_lake_file_system, data_lake_directory):
    try:
        # Set up Azure credentials and clients
        credential = DefaultAzureCredential()
        adf_client = DataFactoryManagementClient(credential, subscription_id)

        # Define the linked services
        linked_service_blob = LinkedServiceReference(reference_name=blob_storage_linked_service, type='LinkedServiceReference')
        linked_service_adls = LinkedServiceReference(reference_name=data_lake_linked_service, type='LinkedServiceReference')

        # Define the source dataset
        blob_storage_dataset = DatasetResource(properties=AzureBlobDataset(
            linked_service_name=linked_service_blob,
            folder_path=blob_container,
            file_name=blob_path
        ))

        # Define the sink dataset
        adls_dataset = DatasetResource(properties=AzureDataLakeStoreDataset(
            linked_service_name=linked_service_adls,
            folder_path=f"{data_lake_file_system}/{data_lake_directory}",
            file_name=blob_path.split('/')[-1]  # Assuming you want to keep the same file name
        ))

        # Create datasets in the Data Factory
        adf_client.datasets.create_or_update(resource_group_name, data_factory_name, 'BlobStorageDataset', blob_storage_dataset)
        adf_client.datasets.create_or_update(resource_group_name, data_factory_name, 'DataLakeStorageDataset', adls_dataset)

        # Create the Copy Activity
        copy_activity = CopyActivity(
            name='CopyFromBlobToDataLake',
            inputs=[DatasetReference(reference_name='BlobStorageDataset', type='DatasetReference')],
            outputs=[DatasetReference(reference_name='DataLakeStorageDataset', type='DatasetReference')],
            source=BlobSource(),
            sink=AzureDataLakeStoreSink()
        )

        # Create the pipeline with the Copy Activity
        pipeline_name = 'BlobToDataLakePipeline'
        pipeline = PipelineResource(activities=[copy_activity])
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
    subscription_id = 'your-subscription-id'  # Replace with your Azure subscription ID
    resource_group_name = 'your-Resource-Group'  # Replace with your resource group name
    data_factory_name = 'your-data-factory'  # Replace with your Data Factory name
    location = 'eastus'  # Replace with your location, e.g., 'eastus'
    data_lake_linked_service  = 'your-linked-service'  # Replace with your linked service name
    storage_account_name = 'your-storage-account'  # Replace with your storage account name
    storage_account_key = 'yourstorageaccountkey'  # Replace with your storage account key

    blob_storage_linked_service_name = 'your-linked-service'  # Replace with your linked service name
    blob_storage_account_name = 'your-storage-account'  # Replace with your storage account name
    blob_storage_account_key = 'yourstorageaccountkey'  # Replace with your storage account key

    blob_container = 'your-blob-container'  # Replace with your Blob container name
    blob_path = 'your-blob-path'  # Replace with your Blob file path
    data_lake_file_system = 'yourfilesystem'  # Replace with your Data Lake file system name
    data_lake_directory = 'yourdirectory'  # Replace with your Data Lake directory

    create_data_factory(subscription_id, resource_group_name, data_factory_name, location)

    create_blob_storage_linked_service(subscription_id, resource_group_name, data_factory_name, data_lake_linked_service , storage_account_name, storage_account_key)
    create_blob_storage_linked_service(subscription_id, resource_group_name, data_factory_name, blob_storage_linked_service_name, blob_storage_account_name, blob_storage_account_key)

    create_data_factory_pipeline(subscription_id, resource_group_name, data_factory_name, blob_storage_linked_service_name, data_lake_linked_service, blob_container, blob_path, data_lake_file_system, data_lake_directory)

    run_pipeline(resource_group_name,data_factory_name,'BlobToDataLakePipeline')
