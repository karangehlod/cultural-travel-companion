"""
Hidden Gems endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List
from pydantic import BaseModel
import structlog

from app.core.security import get_current_user_firebase
from app.models.user import User
from app.models.destination import Destination
from app.models.hidden_gem import HiddenGem
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.gemini import gemini_service, HiddenGemRecommendation

router = APIRouter()
logger = structlog.get_logger()


class HiddenGemDiscoveryRequest(BaseModel):
    destination_name: str
    country: str
    known_places: Optional[List[str]] = None
    interest_areas: Optional[List[str]] = None
    num_gems: int = 5


class HiddenGemResponse(BaseModel):
    id: str
    destination_id: str
    name: str
    description: str
    short_description: Optional[str]
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    cultural_significance: Optional[str]
    local_story: Optional[str]
    discovered_by: Optional[str]
    categories: Optional[str]
    access_difficulty: Optional[str]
    best_time_to_visit: Optional[str]
    visit_duration_minutes: Optional[int]
    photos: Optional[str]
    primary_photo: Optional[str]
    verified_by_local: bool
    verification_notes: Optional[str]
    ai_cultural_narrative: Optional[str]
    ai_local_insights: Optional[str]
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


class HiddenGemDiscoveryResponse(BaseModel):
    name: str
    description: str
    location_hint: str
    cultural_significance: str
    local_story: str
    best_time_to_visit: str
    access_difficulty: str
    visit_duration_hours: float
    what_makes_it_special: str
    local_tips: List[str]


@router.post("/discover", response_model=List[HiddenGemDiscoveryResponse])
async def discover_hidden_gems(
    request: HiddenGemDiscoveryRequest,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Discover hidden cultural gems using AI"""
    try:
        gems = await gemini_service.discover_hidden_gems(
            destination=request.destination_name,
            country=request.country,
            known_places=request.known_places,
            interest_areas=request.interest_areas,
            num_gems=request.num_gems,
        )
        
        return [
            HiddenGemDiscoveryResponse(
                name=g.name,
                description=g.description,
                location_hint=g.location_hint,
                cultural_significance=g.cultural_significance,
                local_story=g.local_story,
                best_time_to_visit=g.best_time_to_visit,
                access_difficulty=g.access_difficulty,
                visit_duration_hours=g.visit_duration_hours,
                what_makes_it_special=g.what_makes_it_special,
                local_tips=g.local_tips,
            )
            for g in gems
        ]
    except Exception as e:
        logger.error("Hidden gem discovery failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to discover hidden gems")


@router.post("/discover/destination/{destination_id}", response_model=List[HiddenGemDiscoveryResponse])
async def discover_gems_for_destination(
    destination_id: str,
    known_places: Optional[List[str]] = None,
    interest_areas: Optional[List[str]] = None,
    num_gems: int = 5,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Discover hidden gems for a saved destination"""
    result = await db.execute(select(Destination).where(Destination.id == destination_id))
    destination = result.scalar_one_or_none()
    
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    try:
        gems = await gemini_service.discover_hidden_gems(
            destination=destination.name,
            country=destination.country,
            known_places=known_places,
            interest_areas=interest_areas,
            num_gems=num_gems,
        )
        
        # Save discovered gems
        for gem in gems:
            hidden_gem = HiddenGem(
                destination_id=destination.id,
                name=gem.name,
                description=gem.description,
                short_description=gem.description[:500],
                address=gem.location_hint,
                cultural_significance=gem.cultural_significance,
                local_story=gem.local_story,
                categories=gem.what_makes_it_special,
                access_difficulty=gem.access_difficulty,
                best_time_to_visit=gem.best_time_to_visit,
                visit_duration_minutes=int(gem.visit_duration_hours * 60),
                ai_cultural_narrative=gem.local_story,
                ai_local_insights=gem.local_tips,
            )
            db.add(hidden_gem)
        
        await db.commit()
        
        return [
            HiddenGemDiscoveryResponse(
                name=g.name,
                description=g.description,
                location_hint=g.location_hint,
                cultural_significance=g.cultural_significance,
                local_story=g.local_story,
                best_time_to_visit=g.best_time_to_visit,
                access_difficulty=g.access_difficulty,
                visit_duration_hours=g.visit_duration_hours,
                what_makes_it_special=g.what_makes_it_special,
                local_tips=g.local_tips,
            )
            for g in gems
        ]
    except Exception as e:
        logger.error("Destination hidden gems failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to discover hidden gems")


@router.get("/destination/{destination_id}", response_model=List[HiddenGemResponse])
async def list_hidden_gems(
    destination_id: str,
    limit: int = 20,
    offset: int = 0,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """List hidden gems for a destination"""
    query = select(HiddenGem).where(HiddenGem.destination_id == destination_id)
    query = query.order_by(HiddenGem.created_at.desc()).offset(offset).limit(limit)
    
    result = await db.execute(query)
    gems = result.scalars().all()
    
    return [
        HiddenGemResponse(
            id=g.id,
            destination_id=g.destination_id,
            name=g.name,
            description=g.description,
            short_description=g.short_description,
            address=g.address,
            latitude=g.latitude,
            longitude=g.longitude,
            cultural_significance=g.cultural_significance,
            local_story=g.local_story,
            discovered_by=g.discovered_by,
            categories=g.categories,
            access_difficulty=g.access_difficulty,
            best_time_to_visit=g.best_time_to_visit,
            visit_duration_minutes=g.visit_duration_minutes,
            photos=g.photos,
            primary_photo=g.primary_photo,
            verified_by_local=g.verified_by_local,
            verification_notes=g.verification_notes,
            ai_cultural_narrative=g.ai_cultural_narrative,
            ai_local_insights=g.ai_local_insights,
            created_at=g.created_at.isoformat(),
            updated_at=g.updated_at.isoformat(),
        )
        for g in gems
    ]