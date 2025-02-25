@echo off
setlocal EnableDelayedExpansion

REM Get full Python path
for /f "tokens=*" %%i in ('where python') do (
    set PYTHON_FULL_PATH=%%i
    goto :check_python
)

:check_python
if not defined PYTHON_FULL_PATH (
    echo Error: Python installation not found
    pause
    exit /b 1
)

echo Found Python at: %PYTHON_FULL_PATH%
"%PYTHON_FULL_PATH%" --version
if errorlevel 1 (
    echo Error: Failed to verify Python installation
    pause
    exit /b 1
)

REM Setup virtual environment directory
set VENV_DIR=%~dp0venv
if not exist "%VENV_DIR%" mkdir "%VENV_DIR%"

echo Creating Python virtual environment using: %PYTHON_FULL_PATH%
echo Target directory: %VENV_DIR%

REM Create virtual environment using full path
"%PYTHON_FULL_PATH%" -m venv "%VENV_DIR%"
if errorlevel 1 (
    echo First attempt failed, trying alternative method...
    "%PYTHON_FULL_PATH%" -m pip install --user virtualenv
    "%PYTHON_FULL_PATH%" -m virtualenv "%VENV_DIR%"
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        echo Debug information:
        echo Python path: %PYTHON_FULL_PATH%
        echo Target directory: %VENV_DIR%
        echo Current directory: %CD%
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

echo Installing required packages...
if exist "%~dp0requirements.txt" (
    pip install -r "%~dp0requirements.txt"
) else (
    echo Warning: requirements.txt not found at %~dp0
    echo Installing core packages only...
    pip install openai
)

echo Setup completed successfully!
echo To activate the virtual environment, run: %VENV_DIR%\Scripts\activate.bat

:end
pause
