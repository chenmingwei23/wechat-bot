"""
Local configuration for the Terminal WeChat Bot.
This file overrides settings from config.py.

IMPORTANT: Rename this file to config_local.py and add your token.
"""

# ======================================================================
# REQUIRED: You need to provide a valid token to use the bot
# ======================================================================
#
# Get a token from: https://wechaty.js.org/docs/puppet-services/
#
# Uncomment and set ONE of these options:

# Option 1: Set the token directly (recommended)
# WECHATY_TOKEN = "your_actual_token_here"

# Option 2: Set the token as an environment variable
# import os
# os.environ['WECHATY_PUPPET_SERVICE_TOKEN'] = 'your_actual_token_here'

# Option 3: Use an endpoint instead of a token
# WECHATY_ENDPOINT = "your_endpoint_here"

# ======================================================================
# Other configuration options (optional)
# ======================================================================

# Bot settings
# BOT_NAME = "My Custom Bot Name"

# Data storage
# DATA_DIR = "custom_data"

# Message settings
# MAX_MESSAGES_IN_MEMORY = 2000
# SAVE_INTERVAL = 600  # 10 minutes

# Logging settings
# LOG_LEVEL = "DEBUG"  # More detailed logs
# LOG_FILE = "custom_log.log"  # Custom log file location 