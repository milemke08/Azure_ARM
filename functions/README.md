# Azure Function for Processing Data in Blob Storage
## 1. Overview
## Title: Azure Function to Process Data in Blob Storage and Save Results Back

This repository contains an Azure Function that processes data stored in Azure Blob Storage and saves the processed results back to Blob Storage. The documentation includes setup instructions, the function code, and error handling.

## 2. Prerequisites
- An Azure account with an active subscription.
- Azure CLI installed.
- Python 3.8 or later installed.
- Azure Functions Core Tools installed.
- Azure Storage account with Blob Storage.
## 3. Setup Instructions
#### Step 1: Create an Azure Function App
Install Azure Functions Core Tools:

```bash
npm install -g azure-functions-core-tools@3 --unsafe-perm true
```

Create a Function App:

```bash
func init ProcessBlobFunctionApp --python
cd .\functions\ProcessBlobFunctionApp\
func new --name ProcessBlobFunction --template "Azure Blob Storage trigger"
```

Update local.settings.json:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "<Your_AzureWebJobsStorage_ConnectionString>",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsBlobInput": "<Your_Input_Container>",
    "AzureWebJobsBlobOutput": "<Your_Output_Container>"
  }
}
```
  #### Step 2: Install Azure SDK for Python
  ```bash
  pip install azure-storage-blob
```
