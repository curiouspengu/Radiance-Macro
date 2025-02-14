@echo off
set installer_dir=%~dp0
setlocal enabledelayedexpansion

rem Define URLs and paths
set python_installer_url=https://www.python.org/ftp/python/3.9.0/python-3.9.0-amd64.exe
set ahk_installer_url=https://www.autohotkey.com/download/ahk-install.exe
set python_install_dir=%ProgramFiles%\Python39
set python_exe=%python_install_dir%\python.exe
set pip_exe=%python_install_dir%\Scripts\pip.exe
set ahk_exe=%ProgramFiles%\AutoHotkey\AutoHotkey.exe

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


@RD /S /Q "%installer_dir%venv\"
python -m venv venv
"%installer_dir%venv\Scripts\pip.exe" install -r "%installer_dir%data\settings\requirements.txt"