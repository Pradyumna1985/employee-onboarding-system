@echo off
setlocal
cd /d "%~dp0"
set "PYTHON_CMD="
set "PYTHON_EXE="

where py >nul 2>nul
if not errorlevel 1 (
    py -3 -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
    if not errorlevel 1 set "PYTHON_CMD=py"
)

if not defined PYTHON_CMD (
    for /f "delims=" %%P in ('where python 2^>nul') do (
        echo %%P | findstr /I /C:"\Microsoft\WindowsApps\python.exe" >nul
        if errorlevel 1 if not defined PYTHON_EXE set "PYTHON_EXE=%%P"
    )
    if defined PYTHON_EXE (
        "%PYTHON_EXE%" -c "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>nul
        if not errorlevel 1 set "PYTHON_CMD=python"
    )
)

if not defined PYTHON_CMD (
    echo Python 3.10 or newer was not found.
    echo Install Python from https://www.python.org/downloads/
    echo During installation, tick "Add python.exe to PATH".
    pause
    exit /b 1
)

if /I "%PYTHON_CMD%"=="py" (
    py -3 -m venv ".venv"
) else (
    "%PYTHON_EXE%" -m venv ".venv"
)
if errorlevel 1 goto :failed

".venv\Scripts\python.exe" -m pip install pyinstaller
if errorlevel 1 goto :failed

call ".venv\Scripts\activate.bat"
if errorlevel 1 goto :failed

pyinstaller --clean --paths . --hidden-import server --hidden-import service --hidden-import content --hidden-import models --hidden-import views --onefile --name "OnboardingSystem" --add-data "static;static" "app.py"
if errorlevel 1 goto :failed

echo.
echo Build complete. The app is at "dist\OnboardingSystem.exe".
pause
exit /b 0

:failed
echo.
echo The build stopped because a step failed. Review the message above.
pause
exit /b 1

