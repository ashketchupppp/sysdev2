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

cd %rootDir%/tests
%venvDir%/Scripts/python.exe -m unittest discover

cd %originalDir%