# Azure_SDK
# Azure Service Principal Setup and Resource Listing

This repository provides instructions and scripts for setting up an Azure Service Principal and using it to list Azure resources.

## Prerequisites

- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- [Python 3.x](https://www.python.org/downloads/)
- [Azure SDK for Python](https://docs.microsoft.com/en-us/python/azure/?view=azure-python)

## Setup Instructions

### 1. Create and Retrieve Azure Service Principal

1. Open a terminal or command prompt.
2. Run the following command to create a new Azure Service Principal. Replace `{subscription-id}` with your actual subscription ID.

    ```bash
    az ad sp create-for-rbac --name "myServicePrincipal" --role contributor --scopes /subscriptions/{subscription-id} --sdk-auth
    ```

3. The command will output JSON with the following details:

    ```json
    {
        "clientId": "your-client-id",
        "clientSecret": "your-client-secret",
        "subscriptionId": "your-subscription-id",
        "tenantId": "your-tenant-id",
        "aadTenantId": "your-tenant-id",
        "resourceManagerEndpointUrl": "https://management.azure.com/"
    }
    ```

4. Copy the `clientId`, `clientSecret`, `tenantId`, and `subscriptionId` values.

### 2. Set Environment Variables

#### Windows

```powershell
setx AZURE_CLIENT_ID "your-client-id"
setx AZURE_CLIENT_SECRET "your-client-secret"
setx AZURE_TENANT_ID "your-tenant-id"
setx AZURE_SUBSCRIPTION_ID "your-subscription-id"
