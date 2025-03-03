"""
Wechaty service for integrating with the WeChat platform.
This service handles message reception, sending, and WeChat login management.
"""
import os
import logging
import asyncio
from typing import List, Optional
from wechaty import Wechaty, Contact, Message, Room
from wechaty.user import Image
import schedule
import time
import threading

# Import configuration and other services
import config as cfg
from app.services.message_service import MessageService
from app.services.ai_service import AiService

logger = logging.getLogger(__name__)

class WechatyService:
    """Service class for Wechaty integration with WeChat."""
    
    def __init__(self):
        """Initialize the Wechaty service."""
        self.bot = Wechaty(
            name=cfg.WECHATY_NAME,
            puppet=cfg.WECHATY_PUPPET,
            puppet_options={
                'token': cfg.WECHATY_TOKEN,
            }
        )
        
        # Initialize other services
        self.message_service = MessageService()
        self.ai_service = AiService()
        
        # Set up event handlers
        self.bot.on('scan', self._on_scan)
        self.bot.on('login', self._on_login)
        self.bot.on('logout', self._on_logout)
        self.bot.on('message', self._on_message)
        self.bot.on('error', self._on_error)
        
        # Scheduler thread for periodic tasks
        self.scheduler_thread = None
        self.is_running = False
    
    async def start(self):
        """Start the Wechaty service."""
        logger.info("Starting Wechaty service...")
        
        # Start the scheduler in a separate thread
        self.is_running = True
        self.scheduler_thread = threading.Thread(target=self._run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()
        
        # Start the Wechaty bot
        await self.bot.start()
    
    async def stop(self):
        """Stop the Wechaty service."""
        logger.info("Stopping Wechaty service...")
        self.is_running = False
        
        if self.bot:
            await self.bot.stop()
    
    def _run_scheduler(self):
        """Run the scheduler for periodic tasks."""
        # Schedule periodic message analysis
        schedule.every(cfg.ANALYSIS_INTERVAL).minutes.do(
            lambda: asyncio.run(self._analyze_messages())
        )
        
        # Run the scheduler loop
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)
    
    async def _analyze_messages(self):
        """Analyze messages periodically."""
        logger.info("Running scheduled message analysis...")
        try:
            # Get recent messages from database
            recent_messages = self.message_service.get_recent_messages(
                limit=cfg.MAX_MESSAGES_PER_ANALYSIS
            )
            
            if recent_messages:
                # Process messages with AI service
                await self.ai_service.analyze_messages(recent_messages)
                logger.info(f"Analyzed {len(recent_messages)} messages")
            else:
                logger.info("No new messages to analyze")
        except Exception as e:
            logger.error(f"Error during message analysis: {e}", exc_info=True)
    
    async def _on_scan(self, qr_code: str, status: int, data: Optional[str] = None):
        """Handle scan events for WeChat login."""
        logger.info(f"Scan QR Code: {status}")
        
        if status == 0:
            # QR code is ready for scanning
            import qrcode
            
            # Generate and save QR code image
            qr = qrcode.QRCode()
            qr.add_data(qr_code)
            qr.make()
            
            qr_img = qr.make_image()
            qr_path = os.path.join(os.path.dirname(cfg.LOG_FILE), "qrcode.png")
            qr_img.save(qr_path)
            
            logger.info(f"QR Code saved to {qr_path}")
            logger.info(f"Please scan the QR Code to log in: {qr_code}")
    
    async def _on_login(self, contact: Contact):
        """Handle login events."""
        logger.info(f"User {contact.name} logged in")
        
        # Get list of rooms (group chats)
        rooms = await self.bot.Room.find_all()
        logger.info(f"Found {len(rooms)} rooms")
        
        # Log room information
        for room in rooms:
            room_id = room.room_id
            topic = await room.topic()
            logger.info(f"Room: {topic} (ID: {room_id})")
    
    async def _on_logout(self, contact: Contact):
        """Handle logout events."""
        logger.info(f"User {contact.name} logged out")
    
    async def _on_message(self, msg: Message):
        """Handle incoming message events."""
        try:
            # Check if message is from a group chat
            room = msg.room()
            if not room:
                return  # Skip non-group messages
            
            # Get room topic
            topic = await room.topic()
            
            # Check if we should monitor this group
            if cfg.MONITORED_GROUPS and topic not in cfg.MONITORED_GROUPS:
                return  # Skip groups not in the monitored list
            
            # Get message information
            sender = msg.talker()
            text = msg.text()
            message_type = msg.type()
            
            logger.debug(f"Received message in {topic} from {sender.name}: {text[:30]}...")
            
            # Store message in database
            await self.message_service.store_message(
                room_id=room.room_id,
                room_topic=topic,
                sender_id=sender.contact_id,
                sender_name=sender.name,
                message_type=str(message_type),
                content=text,
                raw_message=msg
            )
        except Exception as e:
            logger.error(f"Error processing message: {e}", exc_info=True)
    
    async def _on_error(self, error):
        """Handle error events."""
        logger.error(f"Wechaty error: {error}", exc_info=True)
    
    async def send_message(self, room_id: str, message: str):
        """Send a message to a room."""
        try:
            room = await self.bot.Room.find(room_id)
            if room:
                await room.say(message)
                logger.info(f"Sent message to room {room_id}")
                return True
            else:
                logger.warning(f"Room {room_id} not found")
                return False
        except Exception as e:
            logger.error(f"Error sending message: {e}", exc_info=True)
            return False 