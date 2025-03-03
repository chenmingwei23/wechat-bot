# Terminal WeChat Bot

A simple terminal-based WeChat bot that doesn't require Docker. Perfect for users who want a lightweight solution.

## Quick Start

1. **Install Python 3.8+** if you don't have it already

2. **Configure the bot**:
   - Edit `config_local.py` to add your Wechaty token
   - Get a free token from: https://wechaty.js.org/docs/puppet-services/

3. **Run the bot**:
   - **Windows users**: Double-click `run_bot.bat`
   - **Linux/Mac users**: Run `./run_bot.sh` in terminal
   
   These scripts will:
   - Create a virtual environment if needed
   - Install required dependencies
   - Start the bot automatically

4. **Scan the QR code** with your WeChat app to log in

5. **Start chatting!** The bot will display all messages in the terminal

## Manual Setup (Alternative)

If you prefer to set up manually:

1. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

2. **Run the bot**:
   ```
   python wechat_bot.py
   ```

## Available Commands

- `/help` - Show available commands
- `/summary` - Show message statistics
- `/version` - Show bot version

## Configuration

The bot can be configured by editing the following files:

- `config.py` - Default configuration (don't edit this directly)
- `config_local.py` - Your custom configuration (create this by copying `config_local.example.py`)

### Configuration Options

- **Bot Settings**:
  - `BOT_NAME` - Name of the bot
  - `VERSION` - Bot version

- **Data Storage**:
  - `DATA_DIR` - Directory for storing data
  - `MESSAGE_FILE` - File for storing messages
  - `BACKUP_DIR` - Directory for backups

- **Message Settings**:
  - `MAX_MESSAGES_IN_MEMORY` - Maximum number of messages to keep in memory
  - `SAVE_INTERVAL` - How often to save messages (in seconds)

- **Logging Settings**:
  - `LOG_LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  - `LOG_FORMAT` - Format for log messages
  - `LOG_FILE` - File for storing logs

- **Wechaty Settings**:
  - `WECHATY_PUPPET` - Puppet provider to use
  - `WECHATY_TOKEN` - Token for puppet provider (if needed)

## Features

- Terminal-based interface
- No Docker required
- Automatic message saving to JSON files
- Group chat monitoring
- Easy setup scripts for Windows, Linux and Mac
- Configurable settings
- Message backup system

## Troubleshooting

- **Token Issues**: If you see errors about invalid tokens or can't connect to the server:
  - Make sure you've added a valid token in `config_local.py`
  - Check that your token hasn't expired
  - Try getting a new token from the Wechaty website

- **QR Code Issues**: If the QR code doesn't display properly, use the URL provided

- **Login Issues**: WeChat may block automated logins; try using a different account if needed

- **Permission Issues**: On Linux/Mac, if the shell script won't run, try `chmod +x run_bot.sh` to make it executable

- **General Errors**: If you encounter other errors, check the log file in the data directory 