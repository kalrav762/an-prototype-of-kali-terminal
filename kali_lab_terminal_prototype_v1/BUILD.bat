@echo off
setlocal
title Kali Lab Terminal - Builder
echo.
echo ==========================================
echo      KALI LAB TERMINAL v2 BUILDER
echo ==========================================
echo.

where py >nul 2>&1
if %errorlevel%==0 (
    set "PY=py"
) else (
    where python >nul 2>&1
    if %errorlevel%==0 (
        set "PY=python"
    ) else (
        echo ERROR: Python is not installed or not in PATH.
        echo Install Python 3 from python.org and try again.
        pause
        exit /b 1
    )
)

echo Installing/updating PyInstaller...
%PY% -m pip install --upgrade pyinstaller
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Could not install PyInstaller.
    pause
    exit /b 1
)

if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

echo.
echo Building standalone EXE...
%PY% -m PyInstaller --noconfirm --clean --windowed --onefile --name "KaliLabTerminal" kali_lab_terminal.py

if %errorlevel% neq 0 (
    echo.
    echo BUILD FAILED.
    pause
    exit /b 1
)

set "EXE=%CD%\dist\KaliLabTerminal.exe"
if not exist "%EXE%" (
    echo.
    echo ERROR: EXE was not created.
    pause
    exit /b 1
)

echo.
echo Creating Desktop shortcut...

set "SHORTCUT=%USERPROFILE%\Desktop\Kali Lab Terminal.lnk"

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$ws=New-Object -ComObject WScript.Shell; $s=$ws.CreateShortcut([Environment]::GetFolderPath('Desktop') + '\Kali Lab Terminal.lnk'); $s.TargetPath='%EXE%'; $s.WorkingDirectory='%CD%'; $s.Description='Kali Lab Terminal v2'; $s.Save()"

if exist "%SHORTCUT%" (
    echo.
    echo ==========================================
    echo SUCCESS!
    echo ==========================================
    echo.
    echo EXE:
    echo %EXE%
    echo.
    echo Desktop shortcut:
    echo %SHORTCUT%
    echo.
    echo Launching Kali Lab Terminal...
    start "" "%EXE%"
) else (
    echo.
    echo EXE created successfully, but the Desktop shortcut could not be created.
    echo You can launch:
    echo %EXE%
)

echo.
pause
