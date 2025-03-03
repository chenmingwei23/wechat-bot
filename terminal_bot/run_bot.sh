#!/bin/bash

echo "Starting WeChat Terminal Bot..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if ! pip freeze | grep -q "wechaty"; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Create data directories
if [ ! -d "data" ]; then
    echo "Creating data directory..."
    mkdir -p data
fi

if [ ! -d "data/backups" ]; then
    echo "Creating backups directory..."
    mkdir -p data/backups
fi

# Create local config if it doesn't exist
if [ ! -f "config_local.py" ]; then
    echo "Creating local configuration template..."
    cp config_local.example.py config_local.py
    echo
    echo "IMPORTANT: Please edit config_local.py to add your Wechaty token."
    echo "You can get a free token from: https://wechaty.js.org/docs/puppet-services/"
    echo
    read -p "Press Enter to exit..."
    exit 1
fi

# Check if token is configured
if ! grep -v "#" config_local.py | grep -q "WECHATY_TOKEN"; then
    if ! grep -v "#" config_local.py | grep -q "WECHATY_PUPPET_SERVICE_TOKEN"; then
        if ! grep -v "#" config_local.py | grep -q "WECHATY_ENDPOINT"; then
            echo
            echo "WARNING: No Wechaty token or endpoint found in config_local.py"
            echo "The bot will not be able to connect to WeChat without a valid token."
            echo
            echo "Please edit config_local.py to add your Wechaty token."
            echo "You can get a free token from: https://wechaty.js.org/docs/puppet-services/"
            echo
            read -p "Press Enter to continue anyway..."
        fi
    fi
fi

# Run the bot
echo "Starting the bot..."
python wechat_bot.py

# Deactivate virtual environment when done
deactivate 