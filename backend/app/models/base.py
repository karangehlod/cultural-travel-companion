"""
Base models and enums
"""
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, DateTime, ForeignKey, Integer, Float, Boolean, JSON, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

from app.core.database import Base


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class TripStatus(str, enum.Enum):
    DRAFT = "draft"
    PLANNING = "planning"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ExperienceType(str, enum.Enum):
    WORKSHOP = "workshop"
    HOMESTAY = "homestay"
    CRAFT = "craft"
    COOKING_CLASS = "cooking_class"
    CEREMONY = "ceremony"
    FESTIVAL = "festival"
    GUIDED_TOUR = "guided_tour"
    CULTURAL_EXCHANGE = "cultural_exchange"
    VOLUNTEER = "volunteer"
    PERFORMANCE = "performance"
    OTHER = "other"


class CuisineType(str, enum.Enum):
    STREET_FOOD = "street_food"
    FAMILY_RECIPE = "family_recipe"
    RESTAURANT = "restaurant"
    MARKET = "market"
    FARM_TO_TABLE = "farm_to_table"
    COOKING_CLASS = "cooking_class"
    FOOD_TOUR = "food_tour"
    OTHER = "other"