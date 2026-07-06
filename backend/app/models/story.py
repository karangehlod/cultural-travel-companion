"""
Story model
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from app.core.database import Base


class Story(Base):
    """Cultural stories, legends, historical narratives"""
    __tablename__ = "stories"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    destination_id: Mapped[str] = mapped_column(String(36), ForeignKey("destinations.id"), nullable=False, index=True)
    
    # Basic info
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Story type
    story_type: Mapped[str] = mapped_column(String(100), nullable=False)  # legend, history, folklore, personal, oral_history, myth
    categories: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    
    # Cultural context
    culture_of_origin: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    language_of_origin: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    historical_period: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    cultural_significance: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Source
    source: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # local elder, historical record, community member
    source_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # oral, written, archaeological, academic
    collected_by: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    collected_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Location relevance
    specific_location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Media
    audio_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    video_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    photos: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    
    # AI-generated
    ai_generated: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    ai_model: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    ai_prompt: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_cultural_accuracy_reviewed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    destination: Mapped["Destination"] = relationship("Destination", back_populates="stories")