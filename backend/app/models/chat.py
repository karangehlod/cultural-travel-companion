"""
Chat models
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from app.core.database import Base


class ChatSession(Base):
    """Chat session with AI travel companion"""
    __tablename__ = "chat_sessions"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    trip_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("trips.id"), nullable=True)
    
    # Session info
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON - current trip context, preferences
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_message_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="chat_sessions")
    messages: Mapped[List["ChatMessage"]] = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan", order_by="ChatMessage.created_at")


class ChatMessage(Base):
    """Individual chat message"""
    __tablename__ = "chat_messages"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id: Mapped[str] = mapped_column(String(36), ForeignKey("chat_sessions.id"), nullable=False, index=True)
    
    # Message
    role: Mapped[str] = mapped_column(String(20), nullable=False)  # user, assistant, system
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # Metadata
    tokens_used: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    model: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    function_calls: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    function_results: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    
    # References to generated content
    referenced_destinations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array of IDs
    referenced_experiences: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    referenced_events: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    referenced_cuisines: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    referenced_stories: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    session: Mapped["ChatSession"] = relationship("ChatSession", back_populates="messages")