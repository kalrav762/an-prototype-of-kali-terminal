$ErrorActionPreference = "Stop"

Write-Host "=== Kali Lab Terminal v2 Windows Builder ===" -ForegroundColor Cyan

python --version
python -m pip install --upgrade pyinstaller

if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }

python -m PyInstaller `
  --noconfirm `
  --clean `
  --windowed `
  --name "KaliLabTerminal" `
  --onefile `
  kali_lab_terminal.py

Write-Host "`nPortable EXE created:" -ForegroundColor Green
Write-Host "dist\KaliLabTerminal.exe"

$iscc = Get-Command ISCC.exe -ErrorAction SilentlyContinue

if ($iscc) {
    Write-Host "`nInno Setup detected. Building installer..." -ForegroundColor Cyan
    & $iscc.Source "installer.iss"
    Write-Host "`nInstaller created in:" -ForegroundColor Green
    Write-Host "installer_output\KaliLabTerminal_Setup.exe"
} else {
    Write-Host "`nInno Setup was not detected." -ForegroundColor Yellow
    Write-Host "Portable EXE is ready at dist\KaliLabTerminal.exe"
    Write-Host "Install Inno Setup, reopen PowerShell, then run .\build.ps1 again."
}
