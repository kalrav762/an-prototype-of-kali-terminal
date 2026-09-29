#define MyAppName "Kali Lab Terminal"
#define MyAppVersion "2.0.0"
#define MyAppPublisher "Kali Lab Terminal"
#define MyAppExeName "KaliLabTerminal.exe"

[Setup]
AppId={{C7C9F6C7-6C1B-4C6A-8C9A-7E2A1A2B93E1}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\KaliLabTerminal
DefaultGroupName={#MyAppName}
OutputDir=installer_output
OutputBaseFilename=KaliLabTerminal_Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
Uninstallable=yes

[Files]
Source: "dist\KaliLabTerminal.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Kali Lab Terminal"; Filename: "{app}\KaliLabTerminal.exe"
Name: "{autodesktop}\Kali Lab Terminal"; Filename: "{app}\KaliLabTerminal.exe"

[Run]
Filename: "{app}\KaliLabTerminal.exe"; Description: "Launch Kali Lab Terminal"; Flags: nowait postinstall skipifsilent
