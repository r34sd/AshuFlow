@echo off
title AshuFlow - Setup & Installer
color 0B
setlocal EnableDelayedExpansion

echo ==================================================
echo        AshuFlow - Automatic Setup
echo ==================================================
echo.
echo  This will install everything needed to run AshuFlow:
echo    - Python (if not installed)
echo    - All required packages
echo    - FFmpeg (on first app launch)
echo.
echo ==================================================
echo.

:: ====================================================
:: STEP 1: Check for Python
:: ====================================================
echo [1/4] Checking for Python...

:: Try common Python commands
set "PYTHON_CMD="

:: Check "python" command
python --version >nul 2>&1
if %errorlevel%==0 (
    set "PYTHON_CMD=python"
    goto :python_found
)

:: Check "python3" command
python3 --version >nul 2>&1
if %errorlevel%==0 (
    set "PYTHON_CMD=python3"
    goto :python_found
)

:: Check "py" launcher
py -3 --version >nul 2>&1
if %errorlevel%==0 (
    set "PYTHON_CMD=py -3"
    goto :python_found
)

:: Check common install paths directly
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
        goto :python_found
    )
)

:: Python not found - install it
echo.
echo  Python is NOT installed. Installing now...
echo.
goto :install_python

:python_found
echo  [OK] Python found: !PYTHON_CMD!
for /f "tokens=*" %%v in ('!PYTHON_CMD! --version 2^>^&1') do echo       %%v
goto :install_deps

:: ====================================================
:: STEP 2: Install Python
:: ====================================================
:install_python
echo [2/4] Installing Python...
echo.

:: Try winget first (available on Windows 10 1709+ and Windows 11)
winget --version >nul 2>&1
if %errorlevel%==0 (
    echo  Using winget to install Python 3.12...
    echo.
    winget install Python.Python.3.12 --accept-source-agreements --accept-package-agreements --silent
    if %errorlevel%==0 (
        echo.
        echo  [OK] Python installed via winget!

        :: Refresh PATH for this session
        set "PATH=%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts;%PATH%"

        :: Verify
        python --version >nul 2>&1
        if %errorlevel%==0 (
            set "PYTHON_CMD=python"
            goto :install_deps
        )

        :: Try direct path
        if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
            set "PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
            goto :install_deps
        )
    )
    echo  winget install did not succeed, trying direct download...
)

:: Fallback: Download Python installer directly
echo  Downloading Python installer...
echo.

set "PYTHON_INSTALLER=%TEMP%\python_installer.exe"
set "PYTHON_URL=https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe"

:: Try PowerShell download
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%'}" 2>nul

if not exist "%PYTHON_INSTALLER%" (
    :: Try certutil as fallback
    certutil -urlcache -split -f "%PYTHON_URL%" "%PYTHON_INSTALLER%" >nul 2>&1
)

if not exist "%PYTHON_INSTALLER%" (
    echo.
    echo  [ERROR] Could not download Python installer.
    echo  Please install Python manually from: https://www.python.org/downloads/
    echo  IMPORTANT: Check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

echo  Installing Python (this may take a minute)...
echo.

:: Install Python silently with PATH option
"%PYTHON_INSTALLER%" /quiet InstallAllUsers=0 PrependPath=1 Include_test=0 Include_launcher=1

if %errorlevel% neq 0 (
    echo  Silent install failed, launching interactive installer...
    echo  IMPORTANT: Check "Add Python to PATH" at the bottom of the installer!
    echo.
    "%PYTHON_INSTALLER%" PrependPath=1
)

:: Clean up installer
del "%PYTHON_INSTALLER%" 2>nul

:: Refresh PATH
set "PATH=%LOCALAPPDATA%\Programs\Python\Python312;%LOCALAPPDATA%\Programs\Python\Python312\Scripts;%PATH%"

:: Verify Python installation
python --version >nul 2>&1
if %errorlevel%==0 (
    set "PYTHON_CMD=python"
    echo  [OK] Python installed successfully!
    goto :install_deps
)

if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set "PYTHON_CMD=%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    echo  [OK] Python installed successfully!
    goto :install_deps
)

echo.
echo  [ERROR] Python installation could not be verified.
echo  Please restart this script or install Python manually.
echo  Download: https://www.python.org/downloads/
echo.
pause
exit /b 1

:: ====================================================
:: STEP 3: Install Python Dependencies
:: ====================================================
:install_deps
echo.
echo [3/4] Installing required packages...
echo.

:: Ensure pip is available
!PYTHON_CMD! -m ensurepip --default-pip >nul 2>&1

:: Upgrade pip silently
!PYTHON_CMD! -m pip install --upgrade pip -q 2>nul

:: Install from requirements.txt if it exists, otherwise install individually
if exist "%~dp0requirements.txt" (
    echo  Installing from requirements.txt...
    !PYTHON_CMD! -m pip install -r "%~dp0requirements.txt" -q
) else (
    echo  Installing packages individually...
    !PYTHON_CMD! -m pip install customtkinter pillow yt-dlp requests spotdl -q
)

if %errorlevel%==0 (
    echo  [OK] All packages installed!
) else (
    echo  [WARNING] Some packages may have failed. The app will retry on launch.
)

:: ====================================================
:: STEP 4: Create Desktop Shortcut
:: ====================================================
echo.
echo [4/4] Creating desktop shortcut...

set "SHORTCUT=%USERPROFILE%\Desktop\AshuFlow.lnk"
set "SCRIPT_DIR=%~dp0"
set "BAT_FILE=%SCRIPT_DIR%AshuFlow.bat"

:: Create shortcut using PowerShell
powershell -Command "& {$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT%'); $s.TargetPath = '%BAT_FILE%'; $s.WorkingDirectory = '%SCRIPT_DIR:~0,-1%'; $s.Description = 'AshuFlow - Media Downloader'; $s.WindowStyle = 7; $s.Save()}" 2>nul

if exist "%SHORTCUT%" (
    echo  [OK] Desktop shortcut created!
) else (
    echo  [SKIP] Could not create shortcut (non-critical)
)

:: ====================================================
:: DONE
:: ====================================================
echo.
echo ==================================================
echo        Setup Complete!
echo ==================================================
echo.
echo  AshuFlow is ready to use.
echo  You can now:
echo    - Double-click "AshuFlow.bat" to launch
echo    - Use the desktop shortcut
echo    - Run: %PYTHON_CMD% ashuflow.py
echo.
echo  (FFmpeg will be downloaded automatically on first launch)
echo.

:: Ask to launch
set /p "LAUNCH=  Launch AshuFlow now? (Y/N): "
if /i "%LAUNCH%"=="Y" (
    echo.
    echo  Starting AshuFlow...
    cd /d "%~dp0"
    start "" !PYTHON_CMD! ashuflow.py
)

echo.
pause
exit /b 0
