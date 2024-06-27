# Ensure the Az module is imported
Import-Module Az

# Function to load environment variables from .env file
function import-DotEnv {
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
import-DotEnv -path $envFilePath

# Get the tenant ID and subscription ID from environment variables
$subscriptionId = [System.Environment]::GetEnvironmentVariable("SUBSCRIPTION_ID")
$resourceGroupName = [System.Environment]::GetEnvironmentVariable("RESOURCE_GROUP_NAME")
$sqlServerName = [System.Environment]::GetEnvironmentVariable("SQL_SERVER_NAME")

if (-not $resourceGroupName) {
    Write-Output "Resource group not found in .env file."
    exit 1
}

if (-not $subscriptionId) {
    Write-Output "Subscription ID not found in .env file."
    exit 1
}

# Replace with your Azure SQL Server details
# $subscriptionId =  $subscriptionId
# $resourceGroupName = 'your-resource-group'
# $sqlServerName = 'your-sql-server'
location = 'East US'

# Replace with the IP ranges for your Data Factory region
$ipRanges = @(
    "20.42.2.0/23",
    "20.42.4.0/26",
    "20.42.64.0/28",
    "20.49.111.0/29",
    "20.119.28.57/32",
    "20.232.89.104/29",
    "40.71.14.32/28",
    "40.78.229.96/28",
    "2603:1030:210:1::480/121",
    "2603:1030:210:1::500/122",
    "2603:1030:210:1::700/121",
    "2603:1030:210:1::780/122",
    "2603:1030:210:402::330/124",
    "2603:1030:210:802::210/124",
    "2603:1030:210:c02::210/124"
)

Connect-AzAccount -TenantId $tenantId
Set-AzContext -SubscriptionId $subscriptionId

# Create firewall rules for each IP range
foreach ($ipRange in $ipRanges) {
    $ipParts = $ipRange.Split('/')
    $startIp = $ipParts[0]
    $endIp = $startIp
    $ruleName = "AllowDataFactory-$($ipParts[0])"
    
    New-AzSqlServerFirewallRule -ResourceGroupName $resourceGroupName -ServerName $sqlServerName -FirewallRuleName $ruleName -StartIpAddress $startIp -EndIpAddress $endIp
}

Write-Output "Firewall rules added successfully."
