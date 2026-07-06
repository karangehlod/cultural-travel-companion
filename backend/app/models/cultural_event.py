"""
Cultural Event model
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, ForeignKey, Float, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from app.core.database import Base


class CulturalEvent(Base):
    """Cultural events, festivals, ceremonies"""
    __tablename__ = "cultural_events"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    destination_id: Mapped[str] = mapped_column(String(36), ForeignKey("destinations.id"), nullable=False, index=True)
    external_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # Ticketmaster, Eventbrite ID
    external_source: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # ticketmaster, eventbrite, local, manual
    
    # Basic info
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    short_description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Event type
    event_type: Mapped[str] = mapped_column(String(100), nullable=False)  # festival, ceremony, workshop, performance, market, etc.
    categories: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    
    # Dates
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    recurrence_pattern: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)  # yearly, monthly, etc.
    
    # Location
    venue_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    venue_address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Cultural context
    cultural_significance: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    history: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    traditions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    dress_code: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    etiquette: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Practical info
    ticket_required: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    ticket_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    price_range: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    language: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    accessibility_info: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Media
    photos: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    primary_photo: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    video_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Contact
    organizer: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # AI-generated
    ai_cultural_narrative: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_visitor_guide: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_what_to_expect: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_verified_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    destination: Mapped["Destination"] = relationship("Destination", back_populates="cultural_events")