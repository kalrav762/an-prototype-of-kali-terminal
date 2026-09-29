# Kali Lab Terminal v2 — Windows Build

## Easiest build

1. Install Python 3.
2. Put all project files in one folder.
3. Open PowerShell in that folder.
4. Run:

```powershell
.\build.ps1
```

This installs PyInstaller and creates:

```text
dist\KaliLabTerminal.exe
```

## Full installer

Install **Inno Setup** on Windows, then run:

```powershell
.\build.ps1
```

The final installer will be:

```text
installer_output\KaliLabTerminal_Setup.exe
```

The installer creates:
- Start Menu shortcut
- Desktop shortcut
- Normal Windows uninstall entry
- Bundled standalone application

## Notes

The application is a simulated cyber-lab terminal. Its `lab scan` command produces simulated results and does not perform real network scans.
