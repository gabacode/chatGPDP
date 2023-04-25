@echo off

set "delimiters=------------------------------------------------------------"

echo %delimiters%
echo Launching!
echo %delimiters%

:: Get current directory
set "DIR=%~dp0"

:: Create virtualenv
if not exist "%DIR%\venv" (
    py -3 -m venv "%DIR%\venv"
    echo %delimiters%
    echo Virtualenv created
    echo %delimiters%
)

:: Activate env
call "%DIR%\venv\Scripts\activate.bat"

:: Upgrade pip
python -m pip install --upgrade pip

:: Install dependencies
pip install -r "%DIR%\requirements.txt"

:: Install briefcase
pip install briefcase

:: Run the app in dev mode
briefcase dev

:: See if there are errors, if so, exit
if %errorlevel% neq 0 (
    echo %delimiters%
    echo There was an error, exiting...
    echo %delimiters%
    exit /b 1
)

echo %delimiters%
echo See you soon!
echo %delimiters%

:: Deactivate virtualenv
call "%DIR%\venv\Scripts\deactivate.bat"