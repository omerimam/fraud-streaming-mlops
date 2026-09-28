$ErrorActionPreference = "Stop"
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
  Write-Host "Git is not installed or not in PATH." -ForegroundColor Red
  exit 1
}
if (-not (Test-Path ".git")) { git init }
git branch -M main
git add .
$changes = git status --porcelain
if (-not $changes) {
  Write-Host "No new changes to commit." -ForegroundColor Green
  exit 0
}
git commit -m "Initial fraud streaming MLOps project"
Write-Host "Local Git repository is ready. Docker was NOT started." -ForegroundColor Green
Write-Host 'Next: create an empty GitHub repository, then run PUSH_TO_GITHUB.ps1.'
