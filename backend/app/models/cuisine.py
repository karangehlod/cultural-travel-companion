"""
Cuisine model
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, DateTime, ForeignKey, Float, Integer, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

from app.core.database import Base
from app.models.base import CuisineType


class Cuisine(Base):
    """Regional cuisine, dishes, food experiences"""
    __tablename__ = "cuisines"
    
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    destination_id: Mapped[str] = mapped_column(String(36), ForeignKey("destinations.id"), nullable=False, index=True)
    google_place_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # Basic info
    name: Mapped[str] = mapped_column(String(255), nullable=False)  # Dish name or restaurant name
    description: Mapped[str] = mapped_column(Text, nullable=False)
    short_description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Type
    cuisine_type: Mapped[CuisineType] = mapped_column(SQLEnum(CuisineType), nullable=False)
    dish_category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # appetizer, main, dessert, drink, etc.
    
    # Cultural context
    cultural_significance: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    history: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    region_of_origin: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    traditional_occasion: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)  # festival, daily, wedding, etc.
    
    # Ingredients & Preparation
    ingredients: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    allergens: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    dietary_tags: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array (vegetarian, vegan, gluten-free, etc.)
    preparation_method: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cooking_time_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Location (if restaurant/market)
    venue_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # Price & Accessibility
    price_range: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    price_level: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # 0-4
    
    # Media
    photos: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    primary_photo: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # Recipe (if applicable)
    recipe: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON with steps, measurements
    serves: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # AI-generated
    ai_cultural_narrative: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_pairing_suggestions: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON
    ai_local_insights: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    destination: Mapped["Destination"] = relationship("Destination", back_populates="cuisines")