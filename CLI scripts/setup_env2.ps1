# Creates a Python virtual environment, installs requirements, sets the VS Code interpreter
# and creates a `.env` template in the repository root.
#
param(
    [string]$VenvName = ".venv",
    [switch]$Force,
    [string]$PythonExecutable = "python"
)

# Paths
$scriptDir = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
$repoRoot = (Resolve-Path (Join-Path $scriptDir "..")).Path
$venvPath = Join-Path $repoRoot $VenvName


Write-Output "ScriptPath root: $scriptDir"
Write-Output "Repository root: $repoRoot"
Write-Output "venv root: $venvPath"

# Create virtual environment
# Check python availability
try {
    & $PythonExecutable --version 2>$null | Out-Null	# check python exists (run --version, hide output)
} catch {
    Write-ErrAndExit "Python executable '$PythonExecutable' not found. Provide a valid Python on PATH or set -PythonExecutable to the full path." 	# report error and exit
}


if (Test-Path $venvPath) {
    if ($Force) {
        Write-Output "Removing existing virtual environment at $venvPath (because -Force was passed)..."
        Remove-Item -Recurse -Force -Path $venvPath
    } else {
        Write-Output "Virtual environment already exists at: $venvPath"
        Write-Output "Use -Force to recreate, or re-run the installer to only configure interpreter and .env."
    }
}

# Create venv if it doesn't exist
if (-not (Test-Path $venvPath)) {
    Write-Output "Creating virtual environment '$VenvName'..."
    $proc = Start-Process -FilePath $PythonExecutable -ArgumentList "-m","venv",$venvPath -NoNewWindow -Wait -PassThru
    if ($proc.ExitCode -ne 0) { Write-ErrAndExit "Failed to create virtual environment (exit code $($proc.ExitCode))." }
    Write-Output "Virtual environment created at: $venvPath"
} else {
    Write-Output "Using existing virtual environment at: $venvPath"
}


# Determine python executable inside venv
$venvPython = Join-Path $venvPath "Scripts\python.exe"
if (-not (Test-Path $venvPython)) { Write-ErrAndExit "Python executable not found inside venv at: $venvPython" }

# Upgrade pip and install requirements
$requirementsFile = Join-Path $repoRoot "requirements.txt"
if (Test-Path $requirementsFile) {
    Write-Output "Upgrading pip and installing requirements from $requirementsFile..."
    & $venvPython -m pip install --upgrade pip setuptools wheel
    if ($LASTEXITCODE -ne 0) { Write-ErrAndExit "Failed to upgrade pip." }
    & $venvPython -m pip install -r $requirementsFile
    if ($LASTEXITCODE -ne 0) { Write-ErrAndExit "Failed to install requirements from $requirementsFile." }
    Write-Output "Requirements installed successfully."
} else {
    Write-Output "No requirements.txt found at $requirementsFile : skipping pip installs."
}
