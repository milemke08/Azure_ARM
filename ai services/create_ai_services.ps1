param (
    [string]$ResourceGroupName = "myResourceGroup",
    [string]$Location = "eastus",
    [string]$ServiceName = "myTTSService",
    [string]$EnvFilePath = ".env"
)

function Update-EnvFile {
    param (
        [string]$FilePath,
        [string]$TTSServiceKey,
        [string]$TTSServiceEndpoint
    )

    try {
        if (Test-Path -Path $FilePath) {
            $content = Get-Content $FilePath
            if ($content -match "^TTS_SERVICE_KEY=") {
                $content = $content -replace "^TTS_SERVICE_KEY=.*", "TTS_SERVICE_KEY=$TTSServiceKey"
            } else {
                $content += "`nTTS_SERVICE_KEY=$TTSServiceKey"
            }
            if ($content -match "^TTS_SERVICE_ENDPOINT=") {
                $content = $content -replace "^TTS_SERVICE_ENDPOINT=.*", "TTS_SERVICE_ENDPOINT=$TTSServiceEndpoint"
            } else {
                $content += "`nTTS_SERVICE_ENDPOINT=$TTSServiceEndpoint"
            }
            Set-Content -Path $FilePath -Value $content
        } else {
            "TTS_SERVICE_KEY=$TTSServiceKey`nTTS_SERVICE_ENDPOINT=$TTSServiceEndpoint" | Out-File -FilePath $FilePath
        }
    } catch {
        Write-Error "Failed to update .env file: $_"
        exit 1
    }
}

function Create-TTSService {
    param (
        [string]$ResourceGroupName,
        [string]$Location,
        [string]$ServiceName
    )

    try {
        # Create resource group
        az group create --name $ResourceGroupName --location $Location
        if ($LASTEXITCODE -ne 0) { throw "Failed to create resource group" }

        # Create TTS resource
        az cognitiveservices account create `
            --name $ServiceName `
            --resource-group $ResourceGroupName `
            --kind SpeechServices `
            --sku S0 `
            --location $Location `
            --yes
        if ($LASTEXITCODE -ne 0) { throw "Failed to create TTS resource" }

        # Retrieve service key and endpoint
        $TTSServiceKey = az cognitiveservices account keys list `
            --name $ServiceName `
            --resource-group $ResourceGroupName `
            --query "key1" `
            --output tsv
        if ($LASTEXITCODE -ne 0) { throw "Failed to retrieve TTS service key" }

        $TTSServiceEndpoint = az cognitiveservices account show `
            --name $ServiceName `
            --resource-group $ResourceGroupName `
            --query "properties.endpoint" `
            --output tsv
        if ($LASTEXITCODE -ne 0) { throw "Failed to retrieve TTS service endpoint" }

        return @($TTSServiceKey, $TTSServiceEndpoint)

    } catch {
        Write-Error "Error: $_"
        exit 1
    }
}

try {
    # Create TTS service and update the .env file
    $ServiceDetails = Create-TTSService -ResourceGroupName $ResourceGroupName -Location $Location -ServiceName $ServiceName
    Update-EnvFile -FilePath $EnvFilePath -TTSServiceKey $ServiceDetails[0] -TTSServiceEndpoint $ServiceDetails[1]

    Write-Host "Azure Text-to-Speech service created successfully. Keys and endpoint are saved to the .env file."
} catch {
    Write-Error "Failed to create Azure Text-to-Speech service: $_"
    exit 1
}
