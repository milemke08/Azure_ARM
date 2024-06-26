# Ensure the Az module is imported
Import-Module Az

# Ask for the resource group name
$resourceGroupName = Read-Host -Prompt "Enter the name of the Azure resource group to delete"

# Confirm the deletion
$confirmation = Read-Host -Prompt "Are you sure you want to delete the resource group '$resourceGroupName'? Type 'yes' to confirm"

if ($confirmation -eq "yes") {
    try {
        # Connect to Azure
        Connect-AzAccount

        # Delete the resource group
        Remove-AzResourceGroup -Name $resourceGroupName -Force -ErrorAction Stop

        Write-Output "Resource group '$resourceGroupName' has been deleted successfully."
    } catch {
        Write-Output "An error occurred: $_"
    }
} else {
    Write-Output "Operation cancelled. The resource group '$resourceGroupName' was not deleted."
}
