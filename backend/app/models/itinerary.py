"""
Itinerary models
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, ForeignKey, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from app.core.database import Base


class ItineraryDay(Base):
    """Single day in a trip itinerary"""
    __tablename__ = "itinerary_days"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    trip_id: Mapped[str] = mapped_column(String(36), ForeignKey("trips.id"), nullable=False, index=True)
    
    # Day info
    day_number: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    theme: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # cultural immersion, food tour, nature, etc.
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # AI-generated
    ai_day_narrative: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_cultural_insights: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    trip: Mapped["Trip"] = relationship("Trip", back_populates="itinerary_days")
    items: Mapped[List["ItineraryItem"]] = relationship("ItineraryItem", back_populates="day", cascade="all, delete-orphan", order_by="ItineraryItem.start_time")


class ItineraryItem(Base):
    """Single item in a day's itinerary"""
    __tablename__ = "itinerary_items"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    day_id: Mapped[str] = mapped_column(String(36), ForeignKey("itinerary_days.id"), nullable=False, index=True)
    
    # References (optional - can be free-form)
    destination_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("destinations.id"), nullable=True)
    experience_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("experiences.id"), nullable=True)
    hidden_gem_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("hidden_gems.id"), nullable=True)
    cultural_event_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("cultural_events.id"), nullable=True)
    cuisine_id: Mapped[Optional[str]] = mapped_column(String(36), ForeignKey("cuisines.id"), nullable=True)
    
    # Item details
    item_type: Mapped[str] = mapped_column(String(50), nullable=False)  # destination, experience, hidden_gem, event, cuisine, transit, free_time, meal, accommodation
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timing
    start_time: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)  # HH:MM format
    end_time: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Location
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    place_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # Cost
    estimated_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    
    # Transport
    transport_mode: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # walk, drive, transit, taxi, bike
    transport_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    transport_duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    transport_cost: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # AI-generated
    ai_context: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_cultural_tips: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Order
    sort_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    day: Mapped["ItineraryDay"] = relationship("ItineraryDay", back_populates="items")
    experience: Mapped[Optional["Experience"]] = relationship("Experience", back_populates="itinerary_items")