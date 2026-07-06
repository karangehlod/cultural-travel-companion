"""
Trip model
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, ForeignKey, Integer, Float, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from app.core.database import Base
from app.models.base import TripStatus


class Trip(Base):
    """Trip/Itinerary model"""
    __tablename__ = "trips"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    
    # Basic info
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[TripStatus] = mapped_column(SQLEnum(TripStatus), default=TripStatus.DRAFT, nullable=False)
    
    # Dates
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Location
    destination_country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    destination_city: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    destination_region: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    destination_coordinates: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # "lat,lng"
    
    # Budget
    budget_min: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    budget_max: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    currency: Mapped[str] = mapped_column(String(3), default="USD", nullable=False)
    
    # Preferences (JSON)
    travel_style: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    interests: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    group_size: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    pace: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # relaxed, moderate, fast
    
    # AI-generated content
    ai_generated_itinerary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON
    ai_cultural_insights: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_recommendations: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    confirmed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="trips")
    itinerary_days: Mapped[List["ItineraryDay"]] = relationship("ItineraryDay", back_populates="trip", cascade="all, delete-orphan", order_by="ItineraryDay.day_number")