from sqlalchemy import Column, String, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.datetime.utcnow)
    conversations = relationship("Conversation", back_populates="user")

class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    title = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id"))
    role = Column(String)  # "user" or "assistant"
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    conversation = relationship("Conversation", back_populates="messages")
