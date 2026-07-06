"""
Destination model
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, ForeignKey, Float, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from app.core.database import Base


class Destination(Base):
    """Destination model"""
    __tablename__ = "destinations"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    google_place_id: Mapped[Optional[str]] = mapped_column(String(100000), unique=True, index=True, nullable=True)
    
    # Basic info
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    short_description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Location
    country: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    region: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, index=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Categories & Types
    categories: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    place_types: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    cultural_significance: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    unesco_heritage: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Media
    photos: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array of photo URLs
    primary_photo: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Details
    opening_hours: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON
    website: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    review_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    price_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 0-4
    
    # Cultural info
    historical_context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cultural_stories: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    local_tips: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    best_time_to_visit: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    
    # AI-generated
    ai_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_cultural_narrative: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_hidden_gems_nearby: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    saved_by_users: Mapped[List["User"]] = relationship("User", secondary="user_saved_destinations", back_populates="saved_destinations")
    hidden_gems: Mapped[List["HiddenGem"]] = relationship("HiddenGem", back_populates="destination", cascade="all, delete-orphan")
    cultural_events: Mapped[List["CulturalEvent"]] = relationship("CulturalEvent", back_populates="destination", cascade="all, delete-orphan")
    cuisines: Mapped[List["Cuisine"]] = relationship("Cuisine", back_populates="destination", cascade="all, delete-orphan")
    experiences: Mapped[List["Experience"]] = relationship("Experience", back_populates="destination", cascade="all, delete-orphan")
    stories: Mapped[List["Story"]] = relationship("Story", back_populates="destination", cascade="all, delete-orphan")