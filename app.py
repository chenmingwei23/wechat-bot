#!/usr/bin/env python3
"""
Main entry point for the WeChat Group Chat Assistant application.
"""
import os
import logging
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Import configuration
try:
    import config as cfg
except ImportError:
    print("Configuration file not found. Please create config.py or config.local.py.")
    exit(1)

# Configure logging
log_dir = os.path.dirname(cfg.LOG_FILE)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logging.basicConfig(
    level=getattr(logging, cfg.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(cfg.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import services after logging is configured
from app.services.wechaty_service import WechatyService
from app.services.web_service import start_web_server

async def main():
    """Main async function to start the application."""
    logger.info("Starting WeChat Group Chat Assistant...")

    # Initialize and start Wechaty service
    wechaty_service = WechatyService()
    
    # Start the web server in a separate thread
    web_thread = start_web_server()
    
    try:
        # Start the Wechaty bot
        await wechaty_service.start()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, shutting down...")
    except Exception as e:
        logger.error(f"Error in main application: {e}", exc_info=True)
    finally:
        # Perform cleanup
        await wechaty_service.stop()
        logger.info("Application shutdown complete.")

if __name__ == "__main__":
    # Run the main async function
    asyncio.run(main()) 