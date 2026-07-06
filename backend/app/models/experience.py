"""
Experience model
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, ForeignKey, Float, Integer, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from app.core.database import Base
from app.models.base import ExperienceType


class Experience(Base):
    """Authentic cultural experiences - workshops, homestays, craft, etc."""
    __tablename__ = "experiences"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    destination_id: Mapped[str] = mapped_column(String(36), ForeignKey("destinations.id"), nullable=False, index=True)
    google_place_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    external_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # Airbnb Experiences, Viator, etc.
    external_source: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    
    # Basic info
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    short_description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Type
    experience_type: Mapped[ExperienceType] = mapped_column(SQLEnum(ExperienceType), nullable=False)
    categories: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    
    # Host/Provider
    host_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    host_bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    host_languages: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    host_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Cultural context
    cultural_significance: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tradition_preserved: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    community_impact: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Schedule
    duration_hours: Mapped[float] = mapped_column(Float, nullable=False)
    schedule: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON - days, times
    max_group_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    min_group_size: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    
    # Location
    venue_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    meeting_point: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # What's included
    includes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    excludes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    what_to_bring: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    dress_code: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    
    # Requirements
    age_restriction: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    skill_level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # beginner, intermediate, advanced
    physical_requirements: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    accessibility_info: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    language: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Price
    price_per_person: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    price_includes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    
    # Booking
    booking_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    cancellation_policy: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    instant_booking: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    
    # Ratings
    rating: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    review_count: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Media
    photos: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    primary_photo: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    video_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # AI-generated
    ai_cultural_narrative: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_what_to_expect: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_local_insights: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_preparation_tips: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    destination: Mapped["Destination"] = relationship("Destination", back_populates="experiences")
    saved_by_users: Mapped[List["User"]] = relationship("User", secondary="user_saved_experiences", back_populates="saved_experiences")
    itinerary_items: Mapped[List["ItineraryItem"]] = relationship("ItineraryItem", back_populates="experience")