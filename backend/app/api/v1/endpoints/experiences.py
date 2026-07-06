"""
Experiences endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List
from pydantic import BaseModel
import structlog

from app.core.security import get_current_user_firebase
from app.models.user import User
from app.models.destination import Destination
from app.models.experience import Experience, ExperienceType
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.gemini import gemini_service, ExperienceInsight
from app.services.google_places import google_places_service

router = APIRouter()
logger = structlog.get_logger()


class ExperienceResponse(BaseModel):
    id: str
    destination_id: str
    name: str
    description: str
    short_description: Optional[str]
    experience_type: str
    categories: Optional[str]
    host_name: Optional[str]
    host_bio: Optional[str]
    host_languages: Optional[str]
    host_verified: bool
    cultural_significance: Optional[str]
    tradition_preserved: Optional[str]
    community_impact: Optional[str]
    duration_hours: float
    schedule: Optional[str]
    max_group_size: Optional[int]
    min_group_size: int
    venue_name: Optional[str]
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    meeting_point: Optional[str]
    includes: Optional[str]
    excludes: Optional[str]
    what_to_bring: Optional[str]
    dress_code: Optional[str]
    age_restriction: Optional[str]
    skill_level: Optional[str]
    physical_requirements: Optional[str]
    accessibility_info: Optional[str]
    language: Optional[str]
    price_per_person: Optional[float]
    currency: str
    price_includes: Optional[str]
    booking_url: Optional[str]
    cancellation_policy: Optional[str]
    instant_booking: bool
    rating: Optional[float]
    review_count: Optional[int]
    photos: Optional[str]
    primary_photo: Optional[str]
    video_url: Optional[str]
    ai_cultural_narrative: Optional[str]
    ai_what_to_expect: Optional[str]
    ai_local_insights: Optional[str]
    ai_preparation_tips: Optional[str]
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


class ExperienceInsightResponse(BaseModel):
    experience_name: str
    experience_type: str
    description: str
    cultural_significance: str
    tradition_preserved: str
    community_impact: str
    what_to_expect: str
    preparation_tips: List[str]
    local_insights: str
    why_it_matters: str


@router.get("/destination/{destination_id}", response_model=List[ExperienceResponse])
async def list_experiences(
    destination_id: str,
    experience_type: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """List experiences for a destination"""
    query = select(Experience).where(Experience.destination_id == destination_id)
    
    if experience_type:
        query = query.where(Experience.experience_type == experience_type)
    
    query = query.order_by(Experience.created_at.desc()).offset(offset).limit(limit)
    
    result = await db.execute(query)
    experiences = result.scalars().all()
    
    return [
        ExperienceResponse(
            id=e.id,
            destination_id=e.destination_id,
            name=e.name,
            description=e.description,
            short_description=e.short_description,
            experience_type=e.experience_type.value,
            categories=e.categories,
            host_name=e.host_name,
            host_bio=e.host_bio,
            host_languages=e.host_languages,
            host_verified=e.host_verified,
            cultural_significance=e.cultural_significance,
            tradition_preserved=e.tradition_preserved,
            community_impact=e.community_impact,
            duration_hours=e.duration_hours,
            schedule=e.schedule,
            max_group_size=e.max_group_size,
            min_group_size=e.min_group_size,
            venue_name=e.venue_name,
            address=e.address,
            latitude=e.latitude,
            longitude=e.longitude,
            meeting_point=e.meeting_point,
            includes=e.includes,
            excludes=e.excludes,
            what_to_bring=e.what_to_bring,
            dress_code=e.dress_code,
            age_restriction=e.age_restriction,
            skill_level=e.skill_level,
            physical_requirements=e.physical_requirements,
            accessibility_info=e.accessibility_info,
            language=e.language,
            price_per_person=e.price_per_person,
            currency=e.currency,
            price_includes=e.price_includes,
            booking_url=e.booking_url,
            cancellation_policy=e.cancellation_policy,
            instant_booking=e.instant_booking,
            rating=e.rating,
            review_count=e.review_count,
            photos=e.photos,
            primary_photo=e.primary_photo,
            video_url=e.video_url,
            ai_cultural_narrative=e.ai_cultural_narrative,
            ai_what_to_expect=e.ai_what_to_expect,
            ai_local_insights=e.ai_local_insights,
            ai_preparation_tips=e.ai_preparation_tips,
            created_at=e.created_at.isoformat(),
            updated_at=e.updated_at.isoformat(),
        )
        for e in experiences
    ]


@router.get("/search/nearby", response_model=List[dict])
async def search_experiences_nearby(
    lat: float,
    lng: float,
    radius: int = 10000,
    experience_type: Optional[str] = None,
    current_user: dict = Depends(get_current_user_firebase),
):
    """Search for experience providers near a location"""
    try:
        # Search for places that might offer cultural experiences
        types = ["tourist_attraction", "cultural_center", "museum", "art_gallery", 
                "performing_arts_theater", "university", "park"]
        
        if experience_type:
            type_mapping = {
                "workshop": ["art_gallery", "cultural_center", "university"],
                "craft": ["art_gallery", "museum", "cultural_center"],
                "cooking_class": ["restaurant", "cultural_center", "tourist_attraction"],
                "guided_tour": ["tourist_attraction", "museum", "cultural_center"],
                "cultural_exchange": ["cultural_center", "university", "community_center"],
            }
            types = type_mapping.get(experience_type, types)
        
        places = await google_places_service.search_nearby(
            lat=lat,
            lng=lng,
            radius=radius,
            included_types=types,
            max_results=20,
        )
        
        return [
            {
                "place_id": p.place_id,
                "name": p.name,
                "address": p.formatted_address,
                "location": p.location,
                "types": p.types,
                "rating": p.rating,
                "price_level": p.price_level,
                "website": p.website,
                "phone": p.phone,
            }
            for p in places
        ]
    except Exception as e:
        logger.error("Experience search failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to search experiences")


@router.post("/insight", response_model=ExperienceInsightResponse)
async def generate_experience_insight(
    experience_name: str,
    experience_type: str,
    destination: str,
    country: str,
    host_info: Optional[str] = None,
    language: str = "en",
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Generate deep cultural insight for an experience"""
    try:
        insight = await gemini_service.generate_experience_insight(
            experience_name=experience_name,
            experience_type=experience_type,
            destination=destination,
            country=country,
            host_info=host_info,
            language=language,
        )
        
        return ExperienceInsightResponse(
            experience_name=insight.experience_name,
            experience_type=insight.experience_type,
            description=insight.description,
            cultural_significance=insight.cultural_significance,
            tradition_preserved=insight.tradition_preserved,
            community_impact=insight.community_impact,
            what_to_expect=insight.what_to_expect,
            preparation_tips=insight.preparation_tips,
            local_insights=insight.local_insights,
            why_it_matters=insight.why_it_matters,
        )
    except Exception as e:
        logger.error("Experience insight failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate experience insight")


@router.post("/insight/experience/{experience_id}", response_model=ExperienceInsightResponse)
async def generate_insight_for_experience(
    experience_id: str,
    language: str = "en",
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Generate cultural insight for a saved experience"""
    result = await db.execute(select(Experience).where(Experience.id == experience_id))
    experience = result.scalar_one_or_none()
    
    if not experience:
        raise HTTPException(status_code=404, detail="Experience not found")
    
    destination_result = await db.execute(select(Destination).where(Destination.id == experience.destination_id))
    destination = destination_result.scalar_one_or_none()
    
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    try:
        insight = await gemini_service.generate_experience_insight(
            experience_name=experience.name,
            experience_type=experience.experience_type.value,
            destination=destination.name,
            country=destination.country,
            host_info=experience.host_bio,
            language=language,
        )
        
        # Save insight to experience
        experience.ai_cultural_narrative = insight.cultural_significance
        experience.ai_what_to_expect = insight.what_to_expect
        experience.ai_local_insights = insight.local_insights
        experience.ai_preparation_tips = insight.preparation_tips
        await db.commit()
        
        return ExperienceInsightResponse(
            experience_name=insight.experience_name,
            experience_type=insight.experience_type,
            description=insight.description,
            cultural_significance=insight.cultural_significance,
            tradition_preserved=insight.tradition_preserved,
            community_impact=insight.community_impact,
            what_to_expect=insight.what_to_expect,
            preparation_tips=insight.preparation_tips,
            local_insights=insight.local_insights,
            why_it_matters=insight.why_it_matters,
        )
    except Exception as e:
        logger.error("Experience insight failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate experience insight")