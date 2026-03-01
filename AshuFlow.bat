@echo off
title AshuFlow - Media Downloader
cd /d "%~dp0"
setlocal EnableDelayedExpansion

:: Try to find Python
set "PYTHON_CMD="

:: Check "python" in PATH
python --version >nul 2>&1
if %errorlevel%==0 (
    set "PYTHON_CMD=python"
    goto :run
)

:: Check "py" launcher
py -3 --version >nul 2>&1
if %errorlevel%==0 (
    set "PYTHON_CMD=py -3"
    goto :run
)

:: Check common install paths
for %%P in (
    "%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "C:\Python313\python.exe"
    "C:\Python312\python.exe"
    "C:\Python311\python.exe"
    "C:\Python310\python.exe"
) do (
    if exist %%P (
        set "PYTHON_CMD=%%~P"
        goto :run
    )
)

:: Python not found
echo.
echo  Python is not installed on this computer.
echo.
echo  Running setup to install Python and all dependencies...
echo.
if exist "%~dp0setup.bat" (
    call "%~dp0setup.bat"
    exit /b
) else (
    echo  setup.bat not found. Please install Python manually:
    echo  https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:run
!PYTHON_CMD! ashuflow.py
if errorlevel 1 (
    echo.
    echo  AshuFlow encountered an error.
    echo  Try running setup.bat to reinstall dependencies.
    echo.
    pause
)
