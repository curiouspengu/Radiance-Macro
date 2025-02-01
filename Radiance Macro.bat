set dir=%~dp0
if not exist "%dir%/venv" (
    python -m venv venv
    call "%dir%venv\Scripts\activate.bat"
    pip install -r "%dir%data\settings\requirements.txt"
)
call "%dir%venv\Scripts\activate.bat"
"%dir%venv\Scripts\python.exe" "%dir%data\initialize.py"