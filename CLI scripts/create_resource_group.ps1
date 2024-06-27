# Ensure the Az module is imported
Import-Module Az

# Function to load environment variables from .env file
function Import-DotEnv {
    param (
        [string]$path
    )
    if (Test-Path $path) {
        $envVars = Get-Content $path | Where-Object { $_ -match "^[^#]" }  # Ignore comment lines
        foreach ($envVar in $envVars) {
            $name, $value = $envVar -split '=', 2
            [System.Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), [System.EnvironmentVariableTarget]::Process)
        }
    } else {
        Write-Output ".env file not found at path: $path"
        exit 1
    }
}

# Function to update .env file
function Update-DotEnv {
    param (
        [string]$path,
        [string]$resourceGroupName
    )
    if (Test-Path $path) {
        $envContent = Get-Content $path
        $updatedContent = @()
        $envContent | ForEach-Object {
            if ($_ -match "^RESOURCE_GROUP_NAME=") {
                $updatedContent += "RESOURCE_GROUP_NAME=$resourceGroupName"
            } else {
                $updatedContent += $_
            }
        }
        if (-not ($updatedContent -contains "RESOURCE_GROUP_NAME=$resourceGroupName")) {
            $updatedContent += "RESOURCE_GROUP_NAME=$resourceGroupName"
        }
        $updatedContent | Set-Content $path
    } else {
        Write-Output ".env file not found at path: $path"
        exit 1
    }
}

# Load the .env file (assumed to be in the parent directory of the script)
$scriptDir = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
$envFilePath = Join-Path -Path $scriptDir -ChildPath "..\.env"
Import-DotEnv -path $envFilePath

# Get the tenant ID and subscription ID from environment variables
$tenantId = [System.Environment]::GetEnvironmentVariable("TENANT_ID")
$subscriptionId = [System.Environment]::GetEnvironmentVariable("SUBSCRIPTION_ID")

if (-not $tenantId) {
    Write-Output "Tenant ID not found in .env file."
    exit 1
}

if (-not $subscriptionId) {
    Write-Output "Subscription ID not found in .env file."
    exit 1
}

# Prompt for the resource group name
$resourceGroupName = Read-Host -Prompt "Enter the name of the Azure resource group to create"

# Use fixed location "East US"
$location = "East US"

# Connect to Azure using the tenant ID and set the subscription context
Connect-AzAccount -TenantId $tenantId
Set-AzContext -SubscriptionId $subscriptionId

# Create the resource group
try {
    New-AzResourceGroup -Name $resourceGroupName -Location $location -ErrorAction Stop
    Write-Output "Resource group '$resourceGroupName' created successfully in the '$location' region."
    
    # Update the .env file with the new resource group name
    Update-DotEnv -path $envFilePath -resourceGroupName $resourceGroupName
    
    # Call the list_az_resources.ps1 script
    $listScriptPath = Join-Path -Path $scriptDir -ChildPath "list_az_resources.ps1"
    if (Test-Path $listScriptPath) {
        Write-Output "Calling list_az_resources.ps1 script..."
        & $listScriptPath
    } else {
        Write-Output "list_az_resources.ps1 script not found at path: $listScriptPath"
    }
} catch {
    Write-Output "An error occurred while creating the resource group: $_"
}

# Pause to keep the console open
Write-Host "Press any key to exit..."
[System.Console]::ReadKey() | Out-Null
