"""
Configuration settings for the Terminal WeChat Bot
"""

# Bot settings
BOT_NAME = "Terminal WeChat Bot"
VERSION = "1.0.0"

# Data storage
DATA_DIR = "data"
MESSAGE_FILE = f"{DATA_DIR}/messages.json"
BACKUP_DIR = f"{DATA_DIR}/backups"

# Message settings
MAX_MESSAGES_IN_MEMORY = 1000  # Number of messages to keep in memory
SAVE_INTERVAL = 300  # Save messages to file every 300 seconds (5 minutes)

# Logging settings
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = f"{DATA_DIR}/bot.log"  # Set to None to disable file logging

# Command settings
COMMAND_PREFIX = "/"  # Commands start with this character
AVAILABLE_COMMANDS = {
    "help": "Show available commands",
    "summary": "Show message statistics",
    "version": "Show bot version"
}

# Wechaty settings
# You can use different puppet providers:
# - wechaty-puppet-wechat: Browser-based WeChat protocol (not available in pip)
# - wechaty-puppet-service: For using with a Wechaty Puppet Service (recommended)
# - wechaty-puppet-padlocal: For using with PadLocal service (paid)
WECHATY_PUPPET = "wechaty-puppet-service"
# For puppet-service, you need either a token or an endpoint
# You can get a free token from: https://wechaty.js.org/docs/puppet-services/
# IMPORTANT: You must set a token in config_local.py
WECHATY_TOKEN = None  # Set this in config_local.py
WECHATY_ENDPOINT = None  # Alternative to token, set in config_local.py

# Try to load local config if it exists
try:
    from config_local import *
    print("Loaded local configuration")
except ImportError:
    print("Using default configuration") 