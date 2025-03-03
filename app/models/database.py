"""
Database models for the WeChat Group Chat Assistant.
"""
import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Room(Base):
    """Model representing a WeChat group chat."""
    __tablename__ = 'rooms'
    
    id = Column(Integer, primary_key=True)
    room_id = Column(String(255), unique=True, nullable=False, index=True)
    topic = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    def __repr__(self):
        return f"<Room(id={self.id}, room_id='{self.room_id}', topic='{self.topic}')>"

class User(Base):
    """Model representing a WeChat user."""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    
    def __repr__(self):
        return f"<User(id={self.id}, user_id='{self.user_id}', name='{self.name}')>"

class Message(Base):
    """Model representing a message in a WeChat group chat."""
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    room_id = Column(String(255), nullable=False, index=True)
    user_id = Column(String(255), nullable=False, index=True)
    message_type = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    metadata = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.now, index=True)
    
    # Create composite index for efficient querying
    __table_args__ = (
        Index('idx_room_user_created', 'room_id', 'user_id', 'created_at'),
    )
    
    def __repr__(self):
        return f"<Message(id={self.id}, room_id='{self.room_id}', user_id='{self.user_id}')>"

class MessageSummary(Base):
    """Model representing a summary of messages from a time period."""
    __tablename__ = 'message_summaries'
    
    id = Column(Integer, primary_key=True)
    room_id = Column(String(255), nullable=False, index=True)
    summary = Column(Text, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    
    def __repr__(self):
        return f"<MessageSummary(id={self.id}, room_id='{self.room_id}')>"

class Keyword(Base):
    """Model representing keywords extracted from messages."""
    __tablename__ = 'keywords'
    
    id = Column(Integer, primary_key=True)
    room_id = Column(String(255), nullable=False, index=True)
    keyword = Column(String(255), nullable=False, index=True)
    frequency = Column(Integer, default=1)
    last_seen = Column(DateTime, default=datetime.datetime.now)
    created_at = Column(DateTime, default=datetime.datetime.now)
    
    # Create composite index for efficient querying
    __table_args__ = (
        Index('idx_room_keyword', 'room_id', 'keyword', unique=True),
    )
    
    def __repr__(self):
        return f"<Keyword(id={self.id}, room_id='{self.room_id}', keyword='{self.keyword}')>" 