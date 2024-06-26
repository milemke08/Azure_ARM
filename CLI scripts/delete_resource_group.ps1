# Ensure the Az module is imported
Import-Module Az

# Function to load environment variables from .env file
function Load-DotEnv {
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

# Load the .env file (assumed to be in the parent directory of the script)
$scriptDir = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
$envFilePath = Join-Path -Path $scriptDir -ChildPath "..\.env"
Load-DotEnv -path $envFilePath

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
$resourceGroupName = Read-Host -Prompt "Enter the name of the Azure resource group to delete"

# Confirm the deletion
$confirmation = Read-Host -Prompt "Are you sure you want to delete the resource group '$resourceGroupName'? Type 'yes' to confirm"

if ($confirmation -eq "yes") {
    try {
        # Connect to Azure using the tenant ID and set the subscription context
        Connect-AzAccount -TenantId $tenantId
        Set-AzContext -SubscriptionId $subscriptionId

        # Delete the resource group
        Remove-AzResourceGroup -Name $resourceGroupName -Force -ErrorAction Stop

        Write-Output "Resource group '$resourceGroupName' has been deleted successfully."
    } catch {
        Write-Output "An error occurred: $_"
    }
} else {
    Write-Output "Operation cancelled. The resource group '$resourceGroupName' was not deleted."
}

# Pause to keep the console open
Write-Host "Press any key to exit..."
[System.Console]::ReadKey() | Out-Null
