"""
User model
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from app.core.database import Base
from sqlalchemy import Enum as SQLEnum
from app.models.base import UserRole


# Association tables
user_saved_destinations = Table(
    "user_saved_destinations",
    Base.metadata,
    Column("user_id", String(36), ForeignKey("users.id"), primary_key=True),
    Column("destination_id", String(36), ForeignKey("destinations.id"), primary_key=True),
    Column("saved_at", DateTime, default=datetime.utcnow, nullable=False),
    Column("notes", Text, nullable=True),
)

user_saved_experiences = Table(
    "user_saved_experiences",
    Base.metadata,
    Column("user_id", String(36), ForeignKey("users.id"), primary_key=True),
    Column("experience_id", String(36), ForeignKey("experiences.id"), primary_key=True),
    Column("saved_at", DateTime, default=datetime.utcnow, nullable=False),
    Column("notes", Text, nullable=True),
)


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    firebase_uid: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    display_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    photo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.USER, nullable=False)
    
    # Preferences
    travel_style: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string
    interests: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    budget_range: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    dietary_restrictions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    accessibility_needs: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    preferred_languages: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    trips: Mapped[List["Trip"]] = relationship("Trip", back_populates="user", cascade="all, delete-orphan")
    saved_destinations: Mapped[List["Destination"]] = relationship("Destination", secondary=user_saved_destinations, back_populates="saved_by_users")
    saved_experiences: Mapped[List["Experience"]] = relationship("Experience", secondary=user_saved_experiences, back_populates="saved_by_users")
    chat_sessions: Mapped[List["ChatSession"]] = relationship("ChatSession", back_populates="user", cascade="all, delete-orphan")