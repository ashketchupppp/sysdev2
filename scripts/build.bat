@echo off
set originalDir=%cd%
set rootDir=%originalDir%/../
cd %rootDir%

set venvDirname=.venv
set venvDir=%rootDir%/%venvDirname%

if exist .venv/ (
    echo .venv already setup
) else (
    python -m venv .venv
)

%venvDir%/Scripts/pip.exe install -r requirements.txt

if exist %rootDir%/build/ (
    echo build dir already created
) else (
    mkdir %rootDir%/build
)
cd %rootDir%/build

REM %venvDir%/Scripts/python.exe -m PyInstaller %rootDir%/OnlineStoreApp/__main__.py --name OnlineStoreApp --onefile --noconfirm
%venvDir%/Scripts/PyInstaller.exe %rootDir%/__main__.spec

cd %originalDir%