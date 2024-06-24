# Load the .env file from the parent directory
$envFilePath = "../.env"

if (Test-Path $envFilePath) {
    $envContent = Get-Content $envFilePath | Where-Object { $_ -match "^[^#]" }  # Ignore comment lines
    foreach ($line in $envContent) {
        $name, $value = $line -split '=', 2
        [System.Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim())
        Write-Output $name.Trim(), $value.Trim()
    }
} else {
    Write-Output ".env file not found"
    exit 1
}

# Now you can use the variables from the .env file
Write-Output "SERVICE_PRINCIPAL: $SERVICE_PRINCIPAL"