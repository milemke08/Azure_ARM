import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.core.exceptions import AzureError, HttpResponseError, ClientAuthenticationError

def list_resource_groups_and_resources():
    try:
        # Authenticate using the default Azure credentials
        credential = DefaultAzureCredential()

        # Initialize the ResourceManagementClient
        subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
        resource_client = ResourceManagementClient(credential, subscription_id)

        # List all resource groups
        resource_groups = resource_client.resource_groups.list()

        # Check if the resource groups list is populated
        if resource_groups:
            for rg in resource_groups:
                print(f"Resource Group: {rg.name}")
                print("-" * 30)

                # List resources in the resource group
                resources = resource_client.resources.list_by_resource_group(rg.name)
                for resource in resources:
                    print(f"Resource Name: {resource.name}")
                    print(f"Resource Type: {resource.type}")
                    print(f"Resource ID: {resource.id}")
                    print("-" * 20)
        else:
            print("No resource groups found.")
    except ClientAuthenticationError as auth_err:
        print(f"Authentication error: {auth_err}")
    except HttpResponseError as http_err:
        print(f"HTTP error: {http_err}")
    except AzureError as azure_err:
        print(f"Azure error: {azure_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Ensure environment variables are set
    required_env_vars = ["AZURE_CLIENT_ID", "AZURE_CLIENT_SECRET", "AZURE_TENANT_ID", "AZURE_SUBSCRIPTION_ID"]
    
    for var in required_env_vars:
        if not os.getenv(var):
            print(f"Environment variable {var} is not set. Please set it before running the script.")
            exit(1)
    
    list_resource_groups_and_resources()
