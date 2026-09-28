$ErrorActionPreference = "Stop"
$required = @(
  ".gitignore",
  "README.md",
  ".github\workflows\ci.yml",
  ".github\workflows\cd-template.yml",
  "docker-compose.app.yml",
  "docker-compose.full.yml",
  "fastapi_service\Dockerfile",
  "streamlit_app\Dockerfile"
)
$missing = @()
foreach ($file in $required) {
  if (-not (Test-Path $file)) { $missing += $file }
}
if ($missing.Count -gt 0) {
  Write-Host "Missing files:" -ForegroundColor Red
  $missing | ForEach-Object { Write-Host " - $_" }
  exit 1
}
Write-Host "GitHub / CI files are present. Docker was NOT started." -ForegroundColor Green
