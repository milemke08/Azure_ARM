import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccountCreateParameters, Sku, Kind

def create_azure_store_account():
    # Retrieve environment variables
    subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
    resource_group = 'myResourceGroup'
    location = 'eastus'
    storage_account_name = 'mystorageactazuresdk2'

    # Authenticate
    credential = DefaultAzureCredential()
    resource_client = ResourceManagementClient(credential, subscription_id)
    storage_client = StorageManagementClient(credential, subscription_id)

    # Create Resource Group
    resource_client.resource_groups.create_or_update(
        resource_group,
        {"location": location}
    )

    # Create Storage Account
    storage_async_operation = storage_client.storage_accounts.begin_create(
        resource_group,
        storage_account_name,
        StorageAccountCreateParameters(
            sku=Sku(name="Standard_RAGRS"),
            kind=Kind.STORAGE_V2,
            location=location,
        ),
    )

    storage_account = storage_async_operation.result()
    print(f'Storage account {storage_account.name} created successfully.')


if __name__ == "__main__":
    # Ensure environment variables are set
    required_env_vars = ["AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET", "AZURE_TENANT_ID", "AZURE_SUBSCRIPTION_ID"]
    
    for var in required_env_vars:
        if not os.getenv(var):
            print(f"Environment variable {var} is not set. Please set it before running the script.")
            exit(1)
    
    create_azure_store_account()
