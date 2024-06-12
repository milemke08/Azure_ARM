# Azure SDK
# Azure Service Principal Setup and Resource Access

This repository provides instructions and scripts for setting up an Azure Service Principal and using it to access Azure resources.

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

5. The service principal should have at least the "Storage Blob Data Contributor" role to upload files to Blob Storage. You can assign this role using the Azure CLI:
    ```bash
    az role assignment create --assignee <clientId> --role "Storage Blob Data Contributor" --scope /subscriptions/<subscriptionId>/resourceGroups/<resourceGroupName>/providers/Microsoft.Storage/storageAccounts/<storageAccountName>
    ```

### 2. Set Windows Environment Variables

```powershell
setx AZURE_CLIENT_ID "your-client-id"
setx AZURE_CLIENT_SECRET "your-client-secret"
setx AZURE_TENANT_ID "your-tenant-id"
setx AZURE_SUBSCRIPTION_ID "your-subscription-id"
```

### 3. Create Virtual Environemnt & Install requirements.txt

```
python -m venv myenv
myenv\Scripts\activate
pip install -r requirements.txt
```
