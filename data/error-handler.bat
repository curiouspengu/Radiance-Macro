@echo off

echo Starting The Checking Process.
python -c "import my_script" 2>error_log.txt
if %ERRORLEVEL% neq 0 (
    echo Error: Python module or script failed. Checking for missing modules...
    
    rem Read the error log to identify the missing module
    findstr /i "ModuleNotFoundError" error_log.txt > nul
    if %ERRORLEVEL% equ 0 (
        echo Missing module detected. Attempting to install missing module...
        rem Extract module name from error (assuming it's a ModuleNotFoundError)
        for /f "tokens=3 delims=''" %%a in ('findstr /i "ModuleNotFoundError" error_log.txt') do (
            echo Installing module: %%a
            pip install %%a
            if %ERRORLEVEL% neq 0 (
                echo Failed to install module %%a. Exiting...
                exit /b %ERRORLEVEL%
            )
        )
    ) else (
        echo No missing modules. Check error_log.txt for other errors.
    )
    exit /b %ERRORLEVEL%
)

echo Python script ran successfully.
