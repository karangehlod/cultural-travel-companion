"""
Models package - exports all models
"""
from app.models.base import (
    UserRole,
    TripStatus,
    ExperienceType,
    CuisineType,
)

from app.models.user import User, user_saved_destinations, user_saved_experiences
from app.models.trip import Trip
from app.models.destination import Destination
from app.models.hidden_gem import HiddenGem
from app.models.cultural_event import CulturalEvent
from app.models.cuisine import Cuisine
from app.models.experience import Experience
from app.models.story import Story
from app.models.itinerary import ItineraryDay, ItineraryItem
from app.models.chat import ChatSession, ChatMessage

__all__ = [
    "UserRole",
    "TripStatus",
    "ExperienceType",
    "CuisineType",
    "User",
    "user_saved_destinations",
    "user_saved_experiences",
    "Trip",
    "Destination",
    "HiddenGem",
    "CulturalEvent",
    "Cuisine",
    "Experience",
    "Story",
    "ItineraryDay",
    "ItineraryItem",
    "ChatSession",
    "ChatMessage",
]