@echo off

set "delimiters=------------------------------------------------------------"

echo %delimiters%
echo Starting build...
echo %delimiters%

:: Get current directory
set "DIR=%~dp0"

:: Create virtualenv
if not exist "%DIR%\venv" (
    python -m venv "%DIR%\venv"
    echo %delimiters%
    echo Virtualenv created
    echo %delimiters%
)

:: Activate env
call "%DIR%\venv\Scripts\activate"

:: Upgrade pip
python -m pip install --upgrade pip

:: Install dependencies
pip install -r "%DIR%\requirements.txt"

:: Install briefcase
pip install briefcase

:: If the project doesn't have a build directory, create it
if not exist "%DIR%\build" (
    echo %delimiters%
    echo Creating project...
    echo %delimiters%
    briefcase create
)

:: Build for Windows
echo %delimiters%
echo Building for Windows
echo %delimiters%
briefcase build windows

:: If the user wants to run the app, run it
set /p "run=Do you want to run the app? (y/n) "
if /i "%run%"=="y" (
    echo %delimiters%
    echo Running the app...
    echo %delimiters%
    briefcase run
) else (
    echo %delimiters%
    echo See you soon!
    echo %delimiters%
)

:: Deactivate virtualenv
call "%DIR%\venv\Scripts\deactivate"