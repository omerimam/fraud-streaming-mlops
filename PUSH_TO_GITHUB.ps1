param(
  [Parameter(Mandatory=$true)]
  [string]$RepoUrl
)
$ErrorActionPreference = "Stop"
if (-not (Test-Path ".git")) {
  Write-Host "Run INIT_GIT_WINDOWS.ps1 first." -ForegroundColor Red
  exit 1
}
git remote remove origin 2>$null
$global:LASTEXITCODE = 0
git remote add origin $RepoUrl
git branch -M main
git push -u origin main
Write-Host "Push completed. GitHub Actions CI should start automatically." -ForegroundColor Green
