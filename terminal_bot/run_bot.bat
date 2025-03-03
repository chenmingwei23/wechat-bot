@echo off
echo Starting WeChat Terminal Bot...

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher.
    pause
    exit /b
)

REM Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Check if dependencies are installed
pip show wechaty > nul 2>&1
if %errorlevel% neq 0 (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Create data directories
if not exist data (
    echo Creating data directory...
    mkdir data
)

if not exist data\backups (
    echo Creating backups directory...
    mkdir data\backups
)

REM Create local config if it doesn't exist
if not exist config_local.py (
    echo Creating local configuration template...
    copy config_local.example.py config_local.py
    echo.
    echo IMPORTANT: Please edit config_local.py to add your Wechaty token.
    echo You can get a free token from: https://wechaty.js.org/docs/puppet-services/
    echo.
    pause
    exit /b
)

REM Check if token is configured
findstr /C:"WECHATY_TOKEN" config_local.py | findstr /V /C:"#" > nul
if %errorlevel% neq 0 (
    findstr /C:"WECHATY_PUPPET_SERVICE_TOKEN" config_local.py | findstr /V /C:"#" > nul
    if %errorlevel% neq 0 (
        findstr /C:"WECHATY_ENDPOINT" config_local.py | findstr /V /C:"#" > nul
        if %errorlevel% neq 0 (
            echo.
            echo WARNING: No Wechaty token or endpoint found in config_local.py
            echo The bot will not be able to connect to WeChat without a valid token.
            echo.
            echo Please edit config_local.py to add your Wechaty token.
            echo You can get a free token from: https://wechaty.js.org/docs/puppet-services/
            echo.
            pause
        )
    )
)

REM Run the bot with the virtual environment's Python
echo Starting the bot...
venv\Scripts\python wechat_bot.py

pause 