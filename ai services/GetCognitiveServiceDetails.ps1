param (
    [string]$ServiceName = "myTTSService",           # Name of the Cognitive Services account
    [string]$ResourceGroupName = "myResourceGroup", # Name of the resource group
    [string]$OutputJsonPath = "ai services\service_details.json" # Path to save the output JSON
)

function Get-CognitiveServiceDetails {
    param (
        [string]$ServiceName,
        [string]$ResourceGroupName,
        [string]$OutputJsonPath
    )

    try {
        # Run the Azure CLI command and capture the output
        $output = az cognitiveservices account show `
            --name $ServiceName `
            --resource-group $ResourceGroupName `
            --output json

        # Save the output to a JSON file
        Set-Content -Path $OutputJsonPath -Value $output -Encoding UTF8
        Write-Host "Cognitive Services details saved to $OutputJsonPath"
    } catch {
        Write-Error "Failed to retrieve Cognitive Services details: $_"
    }
}

# Main script execution
Get-CognitiveServiceDetails -ServiceName $ServiceName -ResourceGroupName $ResourceGroupName -OutputJsonPath $OutputJsonPath
