param (
    [string]$ResourceGroupName = "myResourceGroup",
    [string]$Location = "eastus",
    [string]$ClusterConfigFilePath = "databricks\cluster_config.json",
    [string]$EnvFilePath = ".env"
)

function Update-EnvFile {
    param (
        [string]$FilePath,
        [string]$WorkspaceName
    )

    try {
        if (Test-Path -Path $FilePath) {
            $content = Get-Content $FilePath
            if ($content -match "^DATABRICKS_WORKSPACE_NAME=") {
                $content = $content -replace "^DATABRICKS_WORKSPACE_NAME=.*", "DATABRICKS_WORKSPACE_NAME=$WorkspaceName"
            } else {
                $content += "`nDATABRICKS_WORKSPACE_NAME=$WorkspaceName"
            }
            Set-Content -Path $FilePath -Value $content
        } else {
            "DATABRICKS_WORKSPACE_NAME=$WorkspaceName" | Out-File -FilePath $FilePath
        }
    } catch {
        Write-Error "Failed to update .env file: $_"
        exit 1
    }
}

function Save-ResourceDetails {
    param (
        [string]$ResourceGroupName,
        [string]$WorkspaceName
    )

    try {
        # Retrieve resource details
        $resourceDetails = az databricks workspace show --name $WorkspaceName --resource-group $ResourceGroupName --output json
        if ($LASTEXITCODE -ne 0) { throw "Failed to retrieve Databricks workspace details." }

        # Parse JSON to get the resource ID
        $resourceDetailsObject = $resourceDetails | ConvertFrom-Json
        $resourceId = $resourceDetailsObject.id

        # Save resource details to a JSON file
        # Define the full directory path where the file will be saved
        $directory = "C:\Users\zdoi\Documents\Python\Azure\AzureSDK\Azure_SDK\databricks\"
        # Define the full file path
        $fileName = Join-Path -Path $directory -ChildPath "$WorkspaceName`_resource_details.json"
        # $fileName = "/databricks/$WorkspaceName`_resource_details.json"
        # $fileName = "$WorkspaceName`_resource_details.json"
        $outputData = @{
            ResourceID = $resourceId
            ResourceDetails = $resourceDetailsObject
        }
        $outputData | ConvertTo-Json -Depth 100 | Set-Content -Path $fileName -Encoding utf8

        Write-Host "Resource details saved to file: $fileName" -ForegroundColor Green
    } catch {
        Write-Error "Error saving resource details: $_"
        exit 1
    }
}


function Create-DatabricksWorkspace {
    param (
        [string]$ResourceGroupName,
        [string]$Location,
        [string]$WorkspaceName,
        [string]$ClusterConfigFilePath
    )

    try {
        # Create resource group
        az group create --name $ResourceGroupName --location $Location
        if ($LASTEXITCODE -ne 0) { throw "Failed to create resource group" }

        # Create databricks workspace
        az databricks workspace create --resource-group $ResourceGroupName --name $WorkspaceName --location $Location --sku standard
        if ($LASTEXITCODE -ne 0) { throw "Failed to create Databricks workspace" }

        # Save resource details
        Save-ResourceDetails -ResourceGroupName $ResourceGroupName -WorkspaceName $WorkspaceName

        # Prompt user to configure Databricks CLI
        Write-Host "Please configure the Databricks CLI by entering the workspace URL and personal access token (PAT)."
        databricks configure --token
        if ($LASTEXITCODE -ne 0) { throw "Failed to configure Databricks CLI" }

        # Create the cluster using the JSON configuration
        databricks clusters create --json-file $ClusterConfigFilePath
        if ($LASTEXITCODE -ne 0) { throw "Failed to create Databricks cluster" }

    } catch {
        Write-Error "Error: $_"
        exit 1
    }
}

try {
    # Prompt for workspace name
    $WorkspaceName = Read-Host "Enter the Databricks workspace name"

    # Update .env file
    Update-EnvFile -FilePath $EnvFilePath -WorkspaceName $WorkspaceName

    # Create Databricks workspace and cluster
    Create-DatabricksWorkspace -ResourceGroupName $ResourceGroupName -Location $Location -WorkspaceName $WorkspaceName -ClusterConfigFilePath $ClusterConfigFilePath

    Write-Host "Databricks workspace and cluster created successfully."
} catch {
    Write-Error "Failed to create Databricks workspace and cluster: $_"
    exit 1
}
