#!/usr/bin/env python3
"""
Simple Terminal-based WeChat Bot.
This is a minimal implementation that doesn't require Docker.
"""
import os
import sys
import asyncio
import logging
from typing import Optional
from datetime import datetime
import json
import time

# Import configuration
try:
    from config import *
except ImportError:
    print("Error: Could not import configuration. Make sure config.py exists.")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler()
    ]
)

# Add file logging if configured
if LOG_FILE:
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger().addHandler(file_handler)

logger = logging.getLogger(__name__)

# Try to import wechaty
try:
    from wechaty import Wechaty, Contact, Message, Room
    from wechaty.user import Image
    from wechaty.wechaty import WechatyOptions
    from wechaty_puppet.schemas.puppet import PuppetOptions
except ImportError as e:
    logger.error(f"Wechaty package import error: {e}")
    logger.error("Wechaty package not found. Please install it with: pip install wechaty wechaty-puppet-service qrcode pillow")
    sys.exit(1)

class TerminalBot:
    """A simple terminal-based WeChat bot."""
    
    def __init__(self):
        """Initialize the terminal bot."""
        # Create options object
        puppet_options = PuppetOptions()
        if WECHATY_TOKEN:
            puppet_options.token = WECHATY_TOKEN
        
        options = WechatyOptions()
        options.puppet = WECHATY_PUPPET
        options.puppet_options = puppet_options
        
        self.bot = Wechaty(options=options)
        
        # Set up event handlers
        self.bot.on('scan', self._on_scan)
        self.bot.on('login', self._on_login)
        self.bot.on('logout', self._on_logout)
        self.bot.on('message', self._on_message)
        self.bot.on('error', self._on_error)
        
        # Message storage (in-memory for MVP)
        self.messages = []
        self.last_save_time = time.time()
        
        # Ensure data directories exist
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(BACKUP_DIR, exist_ok=True)
        
        # Load existing messages if available
        self._load_messages()
    
    def _load_messages(self):
        """Load messages from the JSON file if it exists."""
        try:
            if os.path.exists(MESSAGE_FILE):
                with open(MESSAGE_FILE, 'r', encoding='utf-8') as f:
                    self.messages = json.load(f)
                    logger.info(f"Loaded {len(self.messages)} messages from {MESSAGE_FILE}")
                    
                # Limit the number of messages in memory
                if len(self.messages) > MAX_MESSAGES_IN_MEMORY:
                    # Create a backup before truncating
                    backup_file = os.path.join(BACKUP_DIR, f"messages_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                    with open(backup_file, 'w', encoding='utf-8') as f:
                        json.dump(self.messages, f, ensure_ascii=False, indent=2)
                    
                    # Keep only the most recent messages
                    self.messages = self.messages[-MAX_MESSAGES_IN_MEMORY:]
                    logger.info(f"Truncated messages to {MAX_MESSAGES_IN_MEMORY}, backup saved to {backup_file}")
        except Exception as e:
            logger.error(f"Error loading messages: {e}", exc_info=True)
    
    async def start(self):
        """Start the bot."""
        logger.info(f"Starting {BOT_NAME} v{VERSION}...")
        await self.bot.start()
    
    async def stop(self):
        """Stop the bot."""
        logger.info(f"Stopping {BOT_NAME}...")
        self._save_messages()  # Save messages before stopping
        await self.bot.stop()
    
    async def _on_scan(self, qr_code: str, status: int, data: Optional[str] = None):
        """Handle scan events for WeChat login."""
        logger.info(f"Scan QR Code to log in: {status}")
        
        # For terminal use, we can use a URL to show QR code
        qr_url = f"https://wechaty.js.org/qrcode/{qr_code}"
        print(f"\n\nScan this QR Code with your WeChat app:\n{qr_url}\n\n")
        
        # If qrcode module is available, display QR code in terminal
        try:
            import qrcode
            qr = qrcode.QRCode()
            qr.add_data(qr_code)
            qr.make()
            qr.print_ascii(invert=True)
            print("\nIf the QR code above doesn't display correctly, use the URL instead.\n")
        except ImportError:
            logger.warning("qrcode module not found. Install with: pip install qrcode")
    
    async def _on_login(self, contact: Contact):
        """Handle login events."""
        logger.info(f"User {contact.name} logged in")
        
        # Get list of rooms (group chats)
        rooms = await self.bot.Room.find_all()
        logger.info(f"Found {len(rooms)} rooms")
        
        # Log room information
        for i, room in enumerate(rooms):
            topic = await room.topic()
            logger.info(f"{i+1}. Room: {topic} (ID: {room.room_id})")
    
    async def _on_logout(self, contact: Contact):
        """Handle logout events."""
        logger.info(f"User {contact.name} logged out")
    
    async def _on_message(self, msg: Message):
        """Handle incoming message events."""
        try:
            # Get message information
            text = msg.text()
            message_type = msg.type()
            sender = msg.talker()
            
            # Check if message is from a group chat
            room = msg.room()
            room_topic = "Private Chat"
            
            if room:
                room_topic = await room.topic()
            
            # Print message to terminal
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            source = f"{room_topic}" if room else f"Private: {sender.name}"
            logger.info(f"[{timestamp}] {source} - {sender.name}: {text}")
            
            # Store message in memory
            message_data = {
                "timestamp": timestamp,
                "room": room_topic if room else "Private",
                "room_id": room.room_id if room else None,
                "sender": sender.name,
                "sender_id": sender.contact_id,
                "type": str(message_type),
                "content": text
            }
            self.messages.append(message_data)
            
            # Check if it's time to save messages
            current_time = time.time()
            if current_time - self.last_save_time > SAVE_INTERVAL:
                self._save_messages()
                self.last_save_time = current_time
            
            # Command handling
            if text.startswith(COMMAND_PREFIX):
                await self._handle_command(text, sender, room)
                    
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
    
    async def _handle_command(self, text: str, sender: Contact, room: Optional[Room] = None):
        """Handle bot commands."""
        # Extract command without the prefix
        command = text[len(COMMAND_PREFIX):].strip().lower()
        
        # Split command and arguments
        parts = command.split(maxsplit=1)
        cmd = parts[0]
        args = parts[1] if len(parts) > 1 else ""
        
        # Help command
        if cmd == "help":
            help_text = "Available commands:\n"
            for cmd_name, description in AVAILABLE_COMMANDS.items():
                help_text += f"{COMMAND_PREFIX}{cmd_name} - {description}\n"
            
            if room:
                await room.say(help_text)
            else:
                await sender.say(help_text)
        
        # Summary command
        elif cmd == "summary":
            room_messages = [m for m in self.messages if m.get("room_id") == (room.room_id if room else None)]
            total_messages = len(room_messages)
            unique_senders = len(set(m.get("sender_id") for m in room_messages))
            
            summary_text = f"Message summary for {room.topic() if room else 'private chat'}:\n"
            summary_text += f"Total messages: {total_messages}\n"
            summary_text += f"Unique senders: {unique_senders}\n"
            summary_text += f"Messages in memory: {len(self.messages)} (max: {MAX_MESSAGES_IN_MEMORY})"
            
            if room:
                await room.say(summary_text)
            else:
                await sender.say(summary_text)
        
        # Version command
        elif cmd == "version":
            version_text = f"{BOT_NAME} v{VERSION}"
            
            if room:
                await room.say(version_text)
            else:
                await sender.say(version_text)
        
        # Unknown command
        elif cmd in AVAILABLE_COMMANDS:
            # Command exists but not implemented
            if room:
                await room.say(f"Command '{cmd}' is recognized but not implemented yet.")
            else:
                await sender.say(f"Command '{cmd}' is recognized but not implemented yet.")
        else:
            # Command doesn't exist
            if room:
                await room.say(f"Unknown command: '{cmd}'. Type {COMMAND_PREFIX}help for available commands.")
            else:
                await sender.say(f"Unknown command: '{cmd}'. Type {COMMAND_PREFIX}help for available commands.")
    
    async def _on_error(self, error):
        """Handle error events."""
        logger.error(f"Wechaty error: {error}", exc_info=True)
    
    def _save_messages(self):
        """Save messages to a JSON file."""
        try:
            with open(MESSAGE_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.messages, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved {len(self.messages)} messages to {MESSAGE_FILE}")
        except Exception as e:
            logger.error(f"Error saving messages: {e}", exc_info=True)

async def main():
    """Main function to run the terminal bot."""
    bot = TerminalBot()
    
    try:
        try:
            await bot.start()
        except Exception as e:
            logger.error(f"Error starting bot: {e}")
            logger.error("This is likely due to an invalid token or network connectivity issues.")
            logger.error("To use this bot with WeChat, you need a valid token from https://wechaty.js.org/docs/puppet-services/")
            logger.error("For testing purposes, you can continue without connecting to WeChat.")
            logger.error("Press Ctrl+C to exit.")
        
        # Keep the bot running
        print(f"\n{BOT_NAME} v{VERSION} is running. Press Ctrl+C to exit.\n")
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, shutting down...")
    except Exception as e:
        logger.error(f"Error in main application: {e}", exc_info=True)
    finally:
        await bot.stop()
        logger.info("Bot shutdown complete.")

if __name__ == "__main__":
    # Run the main async function
    asyncio.run(main()) 