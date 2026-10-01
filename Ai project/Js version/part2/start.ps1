$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

docker info *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker Desktop ne tourne pas. Lance-le puis réessaie." -ForegroundColor Red
    exit 1
}

docker compose up --build -d
Start-Process "http://localhost:8080"