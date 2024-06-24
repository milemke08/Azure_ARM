# Load the .env file from the parent directory
$envFilePath = "../.env"

if (Test-Path $envFilePath) {
    $envContent = Get-Content $envFilePath | Where-Object { $_ -match "^[^#]" }  # Ignore comment lines
    foreach ($line in $envContent) {
        $name, $value = $line -split '=', 2
        # [System.Environment]::SetEnvironmentVariable($name.Trim(), $value.Trim())
        # Write-Output $name.Trim(), $value.Trim()

          # Check if the name is "SERVICE_PRINCIPAL" and run az ad sp delete if it is
          if ($name.Trim() -eq "SERVICE_PRINCIPAL") {
            Write-Output "Deleting Service Principal: " $value.Trim()
            az ad sp delete --id $value.Trim()
          }
    }
} else {
    Write-Output ".env file not found"
    exit 1
}

# Now you can use the variables from the .env file
# Write-Output "SERVICE_PRINCIPAL: $SERVICE_PRINCIPAL"

# az ad sp list --display-name <service-principal-name> --query "[].{DisplayName:displayName, AppId:appId, ObjectId:objectId}"
# 