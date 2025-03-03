"""
Configuration file for the WeChat Group Chat Assistant.
Copy this file to config.local.py and edit with your settings.
"""
import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Wechaty Configuration
WECHATY_TOKEN = "your_wechaty_token_here"  # Replace with your Wechaty PadLocal token
WECHATY_PUPPET = "wechaty-puppet-padlocal"
WECHATY_NAME = "wechat-group-assistant"

# OpenAI Configuration
OPENAI_API_KEY = "your_openai_api_key_here"  # Replace with your OpenAI API key
OPENAI_MODEL = "gpt-3.5-turbo"  # Or another model of your choice

# Database Configuration
DB_TYPE = "sqlite"  # "sqlite" or "postgresql"
DB_PATH = os.path.join(BASE_DIR, "data", "wechat_assistant.db")
# For PostgreSQL (if used in production)
# DB_HOST = "localhost"
# DB_PORT = 5432
# DB_NAME = "wechat_assistant"
# DB_USER = "username"
# DB_PASSWORD = "password"

# Web Server Configuration
WEB_HOST = "127.0.0.1"
WEB_PORT = 5000
DEBUG = True

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = os.path.join(BASE_DIR, "logs", "app.log")

# Group Chat Settings
# List of group names to monitor (empty list means all groups)
MONITORED_GROUPS = []

# Message Analysis Settings
# How often to run message analysis (in minutes)
ANALYSIS_INTERVAL = 60
# Maximum number of messages to analyze at once
MAX_MESSAGES_PER_ANALYSIS = 1000

# Load local settings if they exist
try:
    from config.local import *  # noqa
except ImportError:
    pass 