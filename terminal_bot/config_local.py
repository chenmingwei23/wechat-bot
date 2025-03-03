"""
Local configuration for the Terminal WeChat Bot.
This file overrides settings from config.py.
"""

# ======================================================================
# IMPORTANT: You need to provide a valid token to use the bot
# ======================================================================
#
# Get a token from: https://wechaty.js.org/docs/puppet-services/
#
# Then uncomment and set one of these options:

# Option 1: Set the token directly
# WECHATY_TOKEN = "your_actual_token_here"

# Option 2: Set the token as an environment variable
# import os
# os.environ['WECHATY_PUPPET_SERVICE_TOKEN'] = 'your_actual_token_here'

# Option 3: Use an endpoint instead of a token
# WECHATY_ENDPOINT = "your_endpoint_here"

# ======================================================================
# Other configuration options (optional)
# ======================================================================

# Change the puppet provider if needed
# WECHATY_PUPPET = "wechaty-puppet-service"  # Default
# WECHATY_PUPPET = "wechaty-puppet-padlocal"  # Requires paid token

# Logging settings
# LOG_LEVEL = "DEBUG"  # More detailed logs
# LOG_FILE = "custom_log.log"  # Custom log file location

# Set environment variables for Wechaty
# import os

# For testing without a real token, we can use the following environment variable
# This will allow the bot to start, but it won't be able to connect to WeChat
# os.environ['WECHATY_PUPPET_SERVICE_TOKEN'] = 'puppet_padplus_default_token'

# If you have a real token, uncomment and set it here:
# WECHATY_TOKEN = "your_actual_token_here"

# Alternatively, you can use an endpoint:
# WECHATY_ENDPOINT = "your_endpoint_here"

# You can override any other settings from config.py here
# For example:
# LOG_LEVEL = "DEBUG"

# Bot settings
# BOT_NAME = "My Custom Bot Name"

# Data storage
# DATA_DIR = "custom_data"

# Message settings
# MAX_MESSAGES_IN_MEMORY = 2000
# SAVE_INTERVAL = 600  # 10 minutes

# Logging settings
# LOG_LEVEL = "DEBUG"
# LOG_FILE = "custom_log.log" 