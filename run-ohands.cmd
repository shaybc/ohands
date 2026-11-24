@echo off
setlocal
echo Starting OpenHands shell ...

REM #### Set the current folder to the batch folder
cd /d "%~dp0"
if errorlevel 1 (
    echo failed to cd into the ohands folder
    pause
    exit /b 1
)

REM #### make sure the correct python version is installed
echo Checking if python 3.12 pr above is installed
python -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)"
if errorlevel 1 (
    echo Python 3.12 or newer is required. Activate your SDK Python environment first.
    pause
    exit /b 1
)

REM #### if needed recreate the venv
set "NEED_SETUP=0"
if not exist ".\.venv\" set "NEED_SETUP=1"
if "%NEED_SETUP%"=="1" (
    echo Creating python virtual environment
    python.exe -m venv .venv
    if errorlevel 1 (
        echo Failed to install python virtual environment [venv]
        pause
        exit /b 1
    )
) else (
    echo Virtual environment and packages already exist. Skipping setup.
)

REM #### activate the virtual environment
echo Activating the python virtual environment
@call .\.venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate python virtual environment [venv]
    pause
    exit /b 1
)

REM #### install requirements
set "NEED_SETUP=0"
if not exist ".\.venv\Lib\site-packages\litellm\" set "NEED_SETUP=1"
if not exist ".\.venv\Lib\site-packages\openhands\" set "NEED_SETUP=1"
if "%NEED_SETUP%"=="1" (
    echo Installing other required dependencies
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Dependency installation failed. check your PyPi Artifactory setup [C:\Users\Dxxxxxx\pip\pip.ini]
        pause
        exit /b 1
    )
)

REM #### execute the Open-Hands SDK script
echo Calling the oHands script
python .\ohands.py

echo Finished !
pause
exit /b %errorlevel%
