[Setup]
AppName=Планировщик волонтёров
AppVersion=1.0.0
DefaultDirName={autopf}\VolunteersPlanner
DefaultGroupName=Планировщик волонтёров
OutputDir=.
OutputBaseFilename=VolunteersPlanner-Setup
Compression=lzma2
SolidCompression=yes

[Languages]
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
Name: "desktopicon"; Description: "Создать ярлык на рабочем столе"; GroupDescription: "Дополнительные значки:"

[Files]
Source: "build\windows\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Планировщик волонтёров"; Filename: "{app}\volunteers_planner.exe"
Name: "{autodesktop}\Планировщик волонтёров"; Filename: "{app}\volunteers_planner.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\volunteers_planner.exe"; Description: "Запустить Планировщик волонтёров"; Flags: nowait postinstall skipifsilent
