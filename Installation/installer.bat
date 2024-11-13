@echo off
title dSIM Installer
setlocal enabledelayedexpansion

rem Check for admin rights, and request if not an administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting admin privileges...
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

rem Define URLs and paths
set python_installer_url=https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe
set zip_url=https://github.com/steveonly2/Radiance-Macro/archive/refs/heads/main.zip
set ahk_installer_url=https://www.autohotkey.com/download/ahk-install.exe
set zip_name=Radiance-Macro-main.zip
set installer_dir=%~dp0
set extracted_dir=%installer_dir%Radiance-Macro-main
set python_install_dir=%ProgramFiles%\Python312
set python_exe=%python_install_dir%\python.exe
set pip_exe=%python_install_dir%\Scripts\pip.exe
set ahk_exe=%ProgramFiles%\AutoHotkey\AutoHotkey.exe

rem Main menu for installation or uninstallation
:main_menu
echo Welcome to the dSIM V2.0 Installer!
echo 1. Install dSIM V2.0
echo 2. Uninstall dSIM V2.0
echo 3. Exit
set /p choice="Select an option (1-3): "

if "%choice%"=="1" (
    goto install
) else if "%choice%"=="2" (
    goto uninstall
) else if "%choice%"=="3" (
    exit /b
) else (
    echo Invalid option. Please try again.
    goto main_menu
)

:install
echo Would you like to install dSIM V2.0? (Y/N)
set /p user_choice=

if /i "%user_choice%" neq "Y" (
    echo Installation canceled.
    pause
    exit /b
)

rem Check if AutoHotkey is installed
set "ahk_installed="
for %%a in ("%ProgramFiles%\AutoHotkey" "%ProgramFiles(x86)%\AutoHotkey") do (
    if exist "%%a\AutoHotkey.exe" (
        set "ahk_installed=1"
    )
)

if defined ahk_installed (
    echo AutoHotkey is already installed.
) else (
    echo AutoHotkey is not installed. Downloading and installing AutoHotkey...
    curl -L -o "%installer_dir%ahk_installer.exe" %ahk_installer_url%
    if errorlevel 1 (
        echo Failed to download AutoHotkey installer! Exiting.
        pause
        exit /b
    )
    start /wait "" "%installer_dir%ahk_installer.exe" /silent
    if errorlevel 1 (
        echo AutoHotkey installation failed! Exiting.
        pause
        exit /b
    ) else (
        echo AutoHotkey installed successfully.
    )
)

rem Check if Python is installed and its version
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not in PATH. Attempting to install Python...
    curl -L -o "%installer_dir%python_installer.exe" %python_installer_url%
    if errorlevel 1 (
        echo Failed to download Python installer! Exiting.
        pause
        exit /b
    )
    start /wait "" "%installer_dir%python_installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
    if exist "%python_exe%" (
        echo Python installed successfully.
    ) else (
        echo Python installation failed! Attempting to add Python manually to system PATH...
        setx PATH "%python_install_dir%;%PATH%"
        python --version >nul 2>&1
        if %errorlevel% neq 0 (
            echo Failed to set Python in PATH. Please restart and try again.
            pause
            exit /b
        ) else (
            echo Python added to PATH successfully.
        )
    )
) else (
    echo Python is already installed. Checking version...
    for /f "tokens=2 delims= " %%i in ('python --version') do (
        set python_version=%%i
        if "!python_version!"=="3.13.0" (
            echo Found Python version 3.13.0. Uninstalling...
            rmdir /s /q "%python_install_dir%"
            echo Please reinstall with the correct version.
            pause
            exit /b
        )
    )
)

rem Check for pip and install if not available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip is not installed. This should be installed with Python.
    echo Please ensure that you run the Python installer correctly.
    echo Attempting to install pip using get-pip.py...
    curl -L -o "%installer_dir%get-pip.py" https://bootstrap.pypa.io/get-pip.py
    if errorlevel 1 (
        echo Failed to download get-pip.py! Exiting.
        pause
        exit /b
    )
    "%python_exe%" "%installer_dir%get-pip.py"
    if errorlevel 1 (
        echo Failed to install pip! Please ensure Python is installed correctly.
        pause
        exit /b
    ) else (
        echo pip installed successfully.
    )
) else (
    echo pip is already available in PATH.
)

rem Install required Python modules
echo Installing required Python modules. This may take a few moments...
set "modules=opencv-python torch json os py-cord"
for %%m in (%modules%) do (
    "%python_exe%" -c "import %%m" >nul 2>&1
    if %errorlevel% neq 0 (
        echo Installing missing module %%m...
        "%pip_exe%" install %%m
        if errorlevel 1 (
            echo Warning: Skipped installation of %%m due to an error.
        ) else (
            echo Module %%m installed successfully.
        )
    ) else (
        echo Module %%m is already installed. Skipping...
    )
)

rem Download and extract ZIP
echo Downloading Radiance Macro ZIP...
curl -L -o "%installer_dir%%zip_name%" %zip_url%
if not exist "%installer_dir%%zip_name%" (
    echo Download failed! Exiting installer.
    pause
    exit /b
)

echo Extracting ZIP file...
powershell -command "Add-Type -AssemblyName System.IO.Compression.FileSystem; [System.IO.Compression.ZipFile]::ExtractToDirectory('%installer_dir%%zip_name%', '%extracted_dir%')"
if %errorlevel% neq 0 (
    echo Failed to extract the ZIP file! Exiting installer.
    pause
    exit /b
)

rem Clean up by removing downloaded ZIP and installers
del "%installer_dir%%zip_name%"
del "%installer_dir%python_installer.exe"
del "%installer_dir%ahk_installer.exe"
del "%installer_dir%get-pip.py"

echo Installation complete! dSIM V2.0 is now installed.
pause
goto main_menu

:uninstall
echo Uninstalling dSIM V2.0...
set /p user_choice="Are you sure you want to uninstall dSIM V2.0? (Y/N): "
if /i "%user_choice%" neq "Y" (
    echo Uninstallation canceled.
    exit /b
)

rem Remove Python if installed
if exist "%python_exe%" (
    echo Uninstalling Python...
    pushd "%python_install_dir%"
    python -m pip uninstall -y pip
    popd
    rmdir /s /q "%python_install_dir%"
    echo Python uninstalled successfully.
)

rem Remove AutoHotkey if installed
if exist "%ahk_exe%" (
    echo Uninstalling AutoHotkey...
    rmdir /s /q "%ProgramFiles%\AutoHotkey"
    echo AutoHotkey uninstalled successfully.
)

rem Remove the extracted folder
if exist "%extracted_dir%" (
    echo Removing extracted files...
    rmdir /s /q "%extracted_dir%"
)

echo Uninstallation complete.
pause
goto main_menu
