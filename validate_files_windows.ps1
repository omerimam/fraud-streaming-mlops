$ErrorActionPreference = "Stop"

Write-Host "Fraud Docker/CI-CD project file check" -ForegroundColor Cyan

$required = @(
  "docker-compose.app.yml",
  "docker-compose.full.yml",
  ".env.docker.example",
  "fastapi_service\Dockerfile",
  "streamlit_app\Dockerfile",
  "monitoring\prometheus-docker.yml",
  ".github\workflows\ci.yml",
  ".github\workflows\cd-template.yml"
)

$missing = @()
foreach ($file in $required) {
  if (-not (Test-Path $file)) {
    $missing += $file
  }
}

if ($missing.Count -gt 0) {
  Write-Host "Missing files:" -ForegroundColor Red
  $missing | ForEach-Object { Write-Host " - $_" }
  exit 1
}

Write-Host "All Docker/CI-CD files are present." -ForegroundColor Green
Write-Host "Docker was NOT started." -ForegroundColor Yellow
