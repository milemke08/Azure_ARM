import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccountCreateParameters

def main():
    try:
        
        # Set up Azure credentials and clients
        credential = DefaultAzureCredential()
        subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
        resource_client = ResourceManagementClient(credential, subscription_id)
        storage_client = StorageManagementClient(credential, subscription_id)

        # Define parameters
        resource_group_name = os.getenv('RESOURCE_GROUP_NAME')
        location = os.getenv('LOCATION')
        storage_account_name = os.getenv('STORAGE_ACCOUNT_NAME')

        # Create resource group
        # print("Creating resource group...")
        # resource_client.resource_groups.create_or_update(resource_group_name, {'location': location})

        # Create storage account
        print("Creating storage account...")
        storage_parameters = StorageAccountCreateParameters(
            sku={'name': 'Standard_LRS'},
            kind='StorageV2',
            location=location,
            is_hns_enabled=True  # Hierarchical namespace must be enabled for Data Lake Storage Gen2
        )
        print(storage_account_name)
        storage_client.storage_accounts.begin_create(resource_group_name, storage_account_name, storage_parameters).result()

        print("Storage account created successfully!")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    load_dotenv()
    main()
