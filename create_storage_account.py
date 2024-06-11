import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import StorageAccountCreateParameters, Sku, Kind

# Retrieve environment variables
subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
resource_group = 'myResourceGroup'
location = 'eastus'
storage_account_name = 'mystorageaccount'

# Authenticate
credential = DefaultAzureCredential()
storage_client = StorageManagementClient(credential, subscription_id)

# Create Resource Group
resource_client = ResourceManagementClient(credential, subscription_id)
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
