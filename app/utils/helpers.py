"""
Helper utilities for the WeChat Group Chat Assistant.
"""
import os
import logging
import datetime
import json
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

def ensure_directory_exists(directory_path: str) -> bool:
    """
    Ensure that a directory exists, creating it if necessary.
    
    Args:
        directory_path: The path of the directory to check/create
        
    Returns:
        bool: True if directory exists or was created, False otherwise
    """
    try:
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            logger.info(f"Created directory: {directory_path}")
        return True
    except Exception as e:
        logger.error(f"Error creating directory {directory_path}: {e}")
        return False

def parse_datetime(datetime_str: str) -> Optional[datetime.datetime]:
    """
    Parse a datetime string into a datetime object.
    
    Args:
        datetime_str: The datetime string to parse
        
    Returns:
        datetime.datetime: The parsed datetime or None if parsing failed
    """
    try:
        # Try ISO format
        return datetime.datetime.fromisoformat(datetime_str)
    except:
        try:
            # Try common formats
            formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y/%m/%d %H:%M:%S",
                "%d-%m-%Y %H:%M:%S",
                "%d/%m/%Y %H:%M:%S"
            ]
            
            for fmt in formats:
                try:
                    return datetime.datetime.strptime(datetime_str, fmt)
                except:
                    continue
            
            # If all formats failed, return None
            logger.warning(f"Failed to parse datetime: {datetime_str}")
            return None
        except Exception as e:
            logger.error(f"Error parsing datetime {datetime_str}: {e}")
            return None

def safe_json_loads(json_str: str) -> Dict[str, Any]:
    """
    Safely parse a JSON string into a dictionary.
    
    Args:
        json_str: The JSON string to parse
        
    Returns:
        dict: The parsed JSON or an empty dict if parsing failed
    """
    try:
        return json.loads(json_str)
    except Exception as e:
        logger.warning(f"Error parsing JSON: {e}")
        return {}

def format_message_for_display(message: Dict[str, Any]) -> str:
    """
    Format a message dictionary for display.
    
    Args:
        message: The message dictionary
        
    Returns:
        str: Formatted message string
    """
    try:
        sender = message.get('user_name', 'Unknown')
        content = message.get('content', '')
        timestamp = message.get('created_at', '')
        
        if timestamp:
            dt = parse_datetime(timestamp)
            if dt:
                timestamp = dt.strftime("%Y-%m-%d %H:%M:%S")
        
        return f"[{timestamp}] {sender}: {content}"
    except Exception as e:
        logger.error(f"Error formatting message: {e}")
        return str(message)

def chunk_text(text: str, max_length: int = 4000) -> List[str]:
    """
    Split a long text into chunks of approximately equal length.
    
    Args:
        text: The text to split
        max_length: Maximum length of each chunk
        
    Returns:
        list: List of text chunks
    """
    if len(text) <= max_length:
        return [text]
    
    # Split by paragraphs first
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        # If adding this paragraph would exceed max_length, start a new chunk
        if len(current_chunk) + len(para) + 2 > max_length:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = para
        else:
            if current_chunk:
                current_chunk += '\n\n' + para
            else:
                current_chunk = para
    
    # Add the last chunk if not empty
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks 