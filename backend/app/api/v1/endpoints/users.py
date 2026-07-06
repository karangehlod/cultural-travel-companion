"""
Users endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import structlog

from app.core.security import get_current_user_firebase
from app.models.user import User
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter()
logger = structlog.get_logger()


class UserProfileResponse(BaseModel):
    id: str
    firebase_uid: str
    email: str
    display_name: Optional[str] = None
    photo_url: Optional[str] = None
    role: str
    travel_style: Optional[str] = None
    interests: Optional[str] = None
    budget_range: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    accessibility_needs: Optional[str] = None
    preferred_languages: Optional[str] = None
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


class UserPreferencesUpdate(BaseModel):
    travel_style: Optional[str] = None
    interests: Optional[str] = None
    budget_range: Optional[str] = None
    dietary_restrictions: Optional[str] = None
    accessibility_needs: Optional[str] = None
    preferred_languages: Optional[str] = None


@router.get("/me/preferences")
async def get_user_preferences(
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Get current user preferences"""
    firebase_uid = current_user.get("uid") or current_user.get("firebase_uid")
    
    result = await db.execute(select(User).where(User.firebase_uid == firebase_uid))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "travel_style": user.travel_style,
        "interests": user.interests,
        "budget_range": user.budget_range,
        "dietary_restrictions": user.dietary_restrictions,
        "accessibility_needs": user.accessibility_needs,
        "preferred_languages": user.preferred_languages,
    }


@router.patch("/me/preferences")
async def update_user_preferences(
    preferences: UserPreferencesUpdate,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Update current user preferences"""
    firebase_uid = current_user.get("uid") or current_user.get("firebase_uid")
    
    result = await db.execute(select(User).where(User.firebase_uid == firebase_uid))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    update_dict = preferences.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(user, field, value)
    
    await db.commit()
    await db.refresh(user)
    
    return {
        "travel_style": user.travel_style,
        "interests": user.interests,
        "budget_range": user.budget_range,
        "dietary_restrictions": user.dietary_restrictions,
        "accessibility_needs": user.accessibility_needs,
        "preferred_languages": user.preferred_languages,
    }


@router.get("/me/saved-destinations")
async def get_saved_destinations(
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Get user's saved destinations"""
    firebase_uid = current_user.get("uid") or current_user.get("firebase_uid")
    
    result = await db.execute(select(User).where(User.firebase_uid == firebase_uid))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return [
        {
            "id": dest.id,
            "name": dest.name,
            "country": dest.country,
            "city": dest.city,
            "primary_photo": dest.primary_photo,
            "rating": dest.rating,
            "saved_at": saved_at.isoformat() if hasattr(saved_at, 'isoformat') else saved_at,
        }
        for dest, saved_at in zip(user.saved_destinations, [None] * len(user.saved_destinations))
    ]


@router.get("/me/saved-experiences")
async def get_saved_experiences(
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Get user's saved experiences"""
    firebase_uid = current_user.get("uid") or current_user.get("firebase_uid")
    
    result = await db.execute(select(User).where(User.firebase_uid == firebase_uid))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return [
        {
            "id": exp.id,
            "name": exp.name,
            "experience_type": exp.experience_type.value,
            "destination_id": exp.destination_id,
            "primary_photo": exp.primary_photo,
            "price_per_person": exp.price_per_person,
            "rating": exp.rating,
        }
        for exp in user.saved_experiences
    ]