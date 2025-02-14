set dir=%~dp0

@RD /S /Q "%dir%venv\"
python -m venv venv
"%dir%venv\Scripts\pip.exe" install -r "%dir%data\settings\requirements.txt"