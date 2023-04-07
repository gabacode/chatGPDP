@echo off

setlocal enabledelayedexpansion

set delimiters=------------------------------------------------------------

echo !delimiters!
echo Starting build...
echo !delimiters!

:: Get current directory
set "DIR=%~dp0"

:: Create virtualenv
if not exist "%DIR%\venv" (
    python -m venv "%DIR%\venv"
    echo !delimiters!
    echo Virtualenv created
    echo !delimiters!
)

:: Activate env
call "%DIR%\venv\Scripts\activate.bat"

:: Update pip
pip install --upgrade pip

:: Install dependencies
pip install -r "%DIR%\requirements.txt"

:: Install pyinstaller
pip install pyinstaller

:: Run pyinstaller
pyinstaller "%DIR%\specs\single.spec"

:: Deactivate virtualenv
deactivate

echo !delimiters!
echo Build complete
echo !delimiters!