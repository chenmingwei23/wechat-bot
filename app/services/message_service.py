"""
Message service for handling storage and retrieval of WeChat messages.
"""
import logging
import json
import datetime
from typing import List, Dict, Any, Optional
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker

import config as cfg
from app.models.database import Base, Message, Room, User, MessageSummary

logger = logging.getLogger(__name__)

class MessageService:
    """Service for managing message storage and retrieval."""
    
    def __init__(self):
        """Initialize the message service with database connection."""
        # Create database connection
        if cfg.DB_TYPE == "sqlite":
            self.engine = create_engine(f"sqlite:///{cfg.DB_PATH}")
        else:
            # PostgreSQL connection
            self.engine = create_engine(
                f"postgresql://{cfg.DB_USER}:{cfg.DB_PASSWORD}@{cfg.DB_HOST}:{cfg.DB_PORT}/{cfg.DB_NAME}"
            )
        
        # Create tables if they don't exist
        Base.metadata.create_all(self.engine)
        
        # Create session factory
        self.Session = sessionmaker(bind=self.engine)
    
    async def store_message(self, room_id: str, room_topic: str, 
                          sender_id: str, sender_name: str,
                          message_type: str, content: str, 
                          raw_message: Any) -> bool:
        """
        Store a message in the database.
        
        Args:
            room_id: The ID of the room/group
            room_topic: The name/topic of the room/group
            sender_id: The ID of the message sender
            sender_name: The name of the message sender
            message_type: The type of the message
            content: The text content of the message
            raw_message: The raw message object for additional processing
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create a database session
            session = self.Session()
            
            # Check if room exists, create if not
            room = session.query(Room).filter_by(room_id=room_id).first()
            if not room:
                room = Room(
                    room_id=room_id,
                    topic=room_topic,
                    created_at=datetime.datetime.now()
                )
                session.add(room)
                session.commit()
            
            # Check if user exists, create if not
            user = session.query(User).filter_by(user_id=sender_id).first()
            if not user:
                user = User(
                    user_id=sender_id,
                    name=sender_name,
                    created_at=datetime.datetime.now()
                )
                session.add(user)
                session.commit()
            
            # Create message object
            message = Message(
                room_id=room_id,
                user_id=sender_id,
                message_type=message_type,
                content=content,
                created_at=datetime.datetime.now()
            )
            
            # Store additional message metadata as JSON
            try:
                metadata = {
                    'msg_id': getattr(raw_message, 'message_id', None),
                    'timestamp': datetime.datetime.now().isoformat()
                }
                message.metadata = json.dumps(metadata)
            except Exception as e:
                logger.warning(f"Error serializing message metadata: {e}")
            
            # Add and commit the message
            session.add(message)
            session.commit()
            
            logger.debug(f"Stored message from {sender_name} in {room_topic}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing message: {e}", exc_info=True)
            if session:
                session.rollback()
            return False
        finally:
            if session:
                session.close()
    
    def get_recent_messages(self, room_id: Optional[str] = None, 
                           limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get recent messages from the database.
        
        Args:
            room_id: Optional room ID to filter by
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of message dictionaries
        """
        try:
            # Create a database session
            session = self.Session()
            
            # Query messages
            query = session.query(Message)
            
            # Filter by room if specified
            if room_id:
                query = query.filter_by(room_id=room_id)
            
            # Get most recent messages first
            query = query.order_by(desc(Message.created_at)).limit(limit)
            
            # Convert to list of dictionaries
            messages = []
            for msg in query.all():
                # Get related room and user information
                room = session.query(Room).filter_by(room_id=msg.room_id).first()
                user = session.query(User).filter_by(user_id=msg.user_id).first()
                
                room_topic = room.topic if room else "Unknown"
                user_name = user.name if user else "Unknown"
                
                # Parse metadata if available
                metadata = {}
                if msg.metadata:
                    try:
                        metadata = json.loads(msg.metadata)
                    except:
                        pass
                
                # Create message dict
                message_dict = {
                    'id': msg.id,
                    'room_id': msg.room_id,
                    'room_topic': room_topic,
                    'user_id': msg.user_id,
                    'user_name': user_name,
                    'message_type': msg.message_type,
                    'content': msg.content,
                    'metadata': metadata,
                    'created_at': msg.created_at.isoformat()
                }
                
                messages.append(message_dict)
            
            return messages
            
        except Exception as e:
            logger.error(f"Error retrieving messages: {e}", exc_info=True)
            return []
        finally:
            if session:
                session.close()
    
    def store_message_summary(self, room_id: str, summary: str, 
                            start_time: datetime.datetime, 
                            end_time: datetime.datetime) -> bool:
        """
        Store a summary of messages from a specific time range.
        
        Args:
            room_id: The ID of the room/group
            summary: The generated summary text
            start_time: The start time of the summary period
            end_time: The end time of the summary period
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create a database session
            session = self.Session()
            
            # Create summary object
            summary_obj = MessageSummary(
                room_id=room_id,
                summary=summary,
                start_time=start_time,
                end_time=end_time,
                created_at=datetime.datetime.now()
            )
            
            # Add and commit the summary
            session.add(summary_obj)
            session.commit()
            
            logger.info(f"Stored summary for room {room_id} from {start_time} to {end_time}")
            return True
            
        except Exception as e:
            logger.error(f"Error storing message summary: {e}", exc_info=True)
            if session:
                session.rollback()
            return False
        finally:
            if session:
                session.close()
    
    def get_message_summaries(self, room_id: Optional[str] = None, 
                            limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get message summaries from the database.
        
        Args:
            room_id: Optional room ID to filter by
            limit: Maximum number of summaries to retrieve
            
        Returns:
            List of summary dictionaries
        """
        try:
            # Create a database session
            session = self.Session()
            
            # Query summaries
            query = session.query(MessageSummary)
            
            # Filter by room if specified
            if room_id:
                query = query.filter_by(room_id=room_id)
            
            # Get most recent summaries first
            query = query.order_by(desc(MessageSummary.created_at)).limit(limit)
            
            # Convert to list of dictionaries
            summaries = []
            for summary in query.all():
                # Get related room information
                room = session.query(Room).filter_by(room_id=summary.room_id).first()
                room_topic = room.topic if room else "Unknown"
                
                # Create summary dict
                summary_dict = {
                    'id': summary.id,
                    'room_id': summary.room_id,
                    'room_topic': room_topic,
                    'summary': summary.summary,
                    'start_time': summary.start_time.isoformat(),
                    'end_time': summary.end_time.isoformat(),
                    'created_at': summary.created_at.isoformat()
                }
                
                summaries.append(summary_dict)
            
            return summaries
            
        except Exception as e:
            logger.error(f"Error retrieving message summaries: {e}", exc_info=True)
            return []
        finally:
            if session:
                session.close() 