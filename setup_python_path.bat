@echo off
echo 🐍 Adding Python to PATH...

REM Get Python installation directory
for /f "tokens=*" %%i in ('py -c "import sys; import os; print(os.path.dirname(sys.executable))"') do set PYTHON_DIR=%%i
echo Python found at: %PYTHON_DIR%

REM Get Scripts directory
set SCRIPTS_DIR=%PYTHON_DIR%\Scripts
echo Scripts directory: %SCRIPTS_DIR%

REM Add to PATH for current session
set PATH=%PYTHON_DIR%;%SCRIPTS_DIR%;%PATH%

echo ✅ Python added to PATH for current session

REM Test the installation
echo.
echo 🧪 Testing Python installation...
python --version
echo.

echo 📦 Installing required packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo 🎖️ SETUP COMPLETE!
echo.
echo To permanently add Python to PATH:
echo 1. Open System Properties ^> Environment Variables
echo 2. Add to PATH: %PYTHON_DIR%
echo 3. Add to PATH: %SCRIPTS_DIR%
echo.
echo Or run this PowerShell command as Administrator:
echo [Environment]::SetEnvironmentVariable("PATH", "$env:PATH;%PYTHON_DIR%;%SCRIPTS_DIR%", "Machine")

pause
