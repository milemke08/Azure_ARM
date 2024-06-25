# Ensure the Az module is loaded
Import-Module Az

# Array to hold the data
$data = @()

# Get all subscriptions
$subscriptions = Get-AzSubscription

foreach ($subscription in $subscriptions) {
    Set-AzContext -Subscription $subscription.Id
    
    $subscriptionData = @{
        SubscriptionId = $subscription.Id
        SubscriptionName = $subscription.Name
        ResourceGroups = @()
    }
    
    # Get all resource groups in the subscription
    $resourceGroups = Get-AzResourceGroup
    
    foreach ($resourceGroup in $resourceGroups) {
        $resourceGroupData = @{
            ResourceGroupName = $resourceGroup.ResourceGroupName
            Location = $resourceGroup.Location
            Resources = @()
        }
        
        # Get all resources in the resource group
        $resources = Get-AzResource -ResourceGroupName $resourceGroup.ResourceGroupName
        
        foreach ($resource in $resources) {
            $resourceData = @{
                ResourceName = $resource.Name
                ResourceType = $resource.ResourceType
                Location = $resource.Location
            }
            $resourceGroupData.Resources += $resourceData
        }
        
        $subscriptionData.ResourceGroups += $resourceGroupData
    }
    
    $data += $subscriptionData
}

# Convert the data to JSON
$jsonData = $data | ConvertTo-Json -Depth 10

# Write the JSON data to a file
$outputFile = "AzureResources.json"
$jsonData | Out-File -FilePath $outputFile

Write-Output "JSON file with Azure resources has been created: $outputFile"
