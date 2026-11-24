@echo off
setlocal
cd /d "%~dp0"
if errorlevel 1 exit /b 1

python -c "import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)"
if errorlevel 1 (
    echo Python 3.12 or newer is required. Activate your SDK Python environment first.
    exit /b 1
)

if defined AIGW_WHEELHOUSE (
    python -m pip install --no-index --find-links "%AIGW_WHEELHOUSE%" -r "%~dp0requirements.txt"
) else (
    python -m pip install -r "%~dp0requirements.txt"
)
if errorlevel 1 (
    echo Dependency installation failed. For offline installation, set AIGW_WHEELHOUSE to your prepared package folder.
    exit /b 1
)

python "%~dp0ohands.py"
exit /b %errorlevel%
