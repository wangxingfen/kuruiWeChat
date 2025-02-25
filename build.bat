@echo off
call venv\Scripts\activate
pyinstaller --clean build.spec
pause
