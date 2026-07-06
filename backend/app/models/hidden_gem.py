"""
Hidden Gem model
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, ForeignKey, Float, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from app.core.database import Base


class HiddenGem(Base):
    """Hidden gem / off-the-beaten-path location"""
    __tablename__ = "hidden_gems"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    destination_id: Mapped[str] = mapped_column(String(36), ForeignKey("destinations.id"), nullable=False, index=True)
    google_place_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Basic info
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    short_description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Location
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Cultural significance
    cultural_significance: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    local_story: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    discovered_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # local guide, community member, etc.
    
    # Details
    categories: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    access_difficulty: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # easy, moderate, hard
    best_time_to_visit: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    visit_duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Media
    photos: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    primary_photo: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Verification
    verified_by_local: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    verification_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # AI-generated
    ai_cultural_narrative: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_local_insights: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    destination: Mapped["Destination"] = relationship("Destination", back_populates="hidden_gems")