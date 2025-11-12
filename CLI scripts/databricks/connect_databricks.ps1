# Ensure required Az modules are available
Import-Module Az.Accounts -ErrorAction SilentlyContinue
Import-Module Az.Resources -ErrorAction SilentlyContinue

# Function to load environment variables from .env file
function Import-DotEnv {
    param (
        [string]$path
    )
    if (Test-Path $path) {
        $envVars = Get-Content $path | Where-Object { $_ -match "^[^#]" -and $_ -match "=" }
        foreach ($envVar in $envVars) {
            $name, $value = $envVar -split '=', 2
            if ($name -and ($null -ne $value)) {
                [System.Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim(), [System.EnvironmentVariableTarget]::Process)
            }
        }
    } else {
        Write-Output ".env file not found at path: $path"
        exit 1
    }
}

# Script directory and .env (assumed parent directory)
$scriptDir = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
$envFilePath = Join-Path -Path $scriptDir -ChildPath "..\.env"
Import-DotEnv -path $envFilePath

# Read required environment variables
$subscriptionId = [System.Environment]::GetEnvironmentVariable("SUBSCRIPTION_ID")
$tenantId = [System.Environment]::GetEnvironmentVariable("TENANT_ID")
$clientId = [System.Environment]::GetEnvironmentVariable("CLIENT_ID")
$clientSecret = [System.Environment]::GetEnvironmentVariable("CLIENT_SECRET")
$resourceGroupName = [System.Environment]::GetEnvironmentVariable("RESOURCE_GROUP_NAME")
$workspaceName = [System.Environment]::GetEnvironmentVariable("DATABRICKS_WORKSPACE_NAME")

if (-not $subscriptionId) { Write-Output "SUBSCRIPTION_ID not found in .env"; exit 1 }
if (-not $tenantId) { Write-Output "TENANT_ID not found in .env"; exit 1 }
if (-not $workspaceName) { Write-Output "DATABRICKS_WORKSPACE_NAME not found in .env"; exit 1 }

# Authenticate
if ($clientId -and $clientSecret) {
    Write-Output "Authenticating with service principal from .env..."
    $secureSecret = ConvertTo-SecureString $clientSecret -AsPlainText -Force
    $cred = New-Object System.Management.Automation.PSCredential ($clientId, $secureSecret)
    try {
        Connect-AzAccount -ServicePrincipal -Credential $cred -Tenant $tenantId -ErrorAction Stop
    } catch {
        Write-Output "Service principal authentication failed: $_"
        exit 1
    }
} else {
    Write-Output "No service principal credentials found in .env — prompting interactive login..."
    Connect-AzAccount -TenantId $tenantId
}

if ($subscriptionId) { Set-AzContext -SubscriptionId $subscriptionId }

# Locate the Databricks workspace resource
try {
    $workspace = Get-AzResource -ResourceGroupName $resourceGroupName -ResourceType 'Microsoft.Databricks/workspaces' -Name $workspaceName -ErrorAction Stop
} catch {
    Write-Output "Failed to find Databricks workspace '$workspaceName' in resource group '$resourceGroupName': $_"
    exit 1
}

# Try to extract the workspace URL (the workspace resource property is commonly 'workspaceUrl')
$workspaceUrl = $null
if ($workspace.Properties) {
    $propNames = $workspace.Properties.PSObject.Properties.Name
    if ($propNames -contains 'workspaceUrl') {
        $workspaceUrl = $workspace.Properties.workspaceUrl
    }
}

if ($workspaceUrl) {
    $databricksWorkspaceUrl = "https://$workspaceUrl"
    Write-Output "Databricks workspace found: $databricksWorkspaceUrl"
    # Export DATABRICKS_HOST for process (useful for local Databricks CLI or other scripts)
    [System.Environment]::SetEnvironmentVariable("DATABRICKS_HOST", $databricksWorkspaceUrl, [System.EnvironmentVariableTarget]::Process)
    [System.Environment]::SetEnvironmentVariable("DATABRICKS_WORKSPACE_NAME", $workspaceName, [System.EnvironmentVariableTarget]::Process)
    # Open in default browser
    try {
        Start-Process -FilePath $databricksWorkspaceUrl
    } catch {
        Write-Output "Unable to open browser. Workspace URL: $databricksWorkspaceUrl"
    }
} else {
    Write-Output "Workspace found but workspace URL not available in resource properties. Here are the properties:"
    $workspace.Properties | ConvertTo-Json -Depth 5 | Write-Output
}

Write-Output "Done."
