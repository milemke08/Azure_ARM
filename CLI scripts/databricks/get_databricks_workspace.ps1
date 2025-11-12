# Ensure required Az modules are available
Import-Module Az.Accounts -ErrorAction SilentlyContinue
Import-Module Az.Resources -ErrorAction SilentlyContinue

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

$scriptDir = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
$envFilePath = Join-Path -Path $scriptDir -ChildPath "..\.env"
Import-DotEnv -path $envFilePath

$subscriptionId = [System.Environment]::GetEnvironmentVariable("SUBSCRIPTION_ID")
$tenantId = [System.Environment]::GetEnvironmentVariable("TENANT_ID")
$resourceGroupName = [System.Environment]::GetEnvironmentVariable("RESOURCE_GROUP_NAME")
$workspaceName = [System.Environment]::GetEnvironmentVariable("DATABRICKS_WORKSPACE_NAME")

if (-not $subscriptionId) { Write-Output "SUBSCRIPTION_ID not found in .env"; exit 1 }
if (-not $tenantId) { Write-Output "TENANT_ID not found in .env"; exit 1 }
if (-not $workspaceName) { Write-Output "DATABRICKS_WORKSPACE_NAME not found in .env"; exit 1 }

Write-Output "Setting context to subscription: $subscriptionId"
if ($subscriptionId) { Set-AzContext -SubscriptionId $subscriptionId }

try {
    $workspace = Get-AzResource -ResourceGroupName $resourceGroupName -ResourceType 'Microsoft.Databricks/workspaces' -Name $workspaceName -ErrorAction Stop
    $workspace | ConvertTo-Json -Depth 6 | Out-File -FilePath "$scriptDir\${workspaceName}_workspace.json"
    Write-Output "Workspace details written to: $scriptDir\${workspaceName}_workspace.json"
} catch {
    Write-Output "Failed to retrieve workspace: $_"
    exit 1
}
