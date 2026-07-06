"""
Cultural Events endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
import structlog

from app.core.security import get_current_user_firebase
from app.models.user import User
from app.models.destination import Destination
from app.models.cultural_event import CulturalEvent
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.gemini import gemini_service, CulturalEventInsight
from app.services.google_places import google_places_service

router = APIRouter()
logger = structlog.get_logger()


class EventSearchRequest(BaseModel):
    destination_name: str
    country: str
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    event_types: Optional[List[str]] = None


class CulturalEventResponse(BaseModel):
    id: str
    destination_id: str
    name: str
    description: str
    short_description: Optional[str]
    event_type: str
    categories: Optional[str]
    start_date: str
    end_date: Optional[str]
    is_recurring: bool
    recurrence_pattern: Optional[str]
    venue_name: Optional[str]
    venue_address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    cultural_significance: Optional[str]
    history: Optional[str]
    traditions: Optional[str]
    dress_code: Optional[str]
    etiquette: Optional[str]
    ticket_required: bool
    ticket_url: Optional[str]
    price_range: Optional[str]
    capacity: Optional[int]
    language: Optional[str]
    accessibility_info: Optional[str]
    photos: Optional[str]
    primary_photo: Optional[str]
    video_url: Optional[str]
    organizer: Optional[str]
    contact_email: Optional[str]
    contact_phone: Optional[str]
    website: Optional[str]
    ai_cultural_narrative: Optional[str]
    ai_visitor_guide: Optional[str]
    ai_what_to_expect: Optional[str]
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


class EventInsightResponse(BaseModel):
    event_name: str
    cultural_significance: str
    history_and_origins: str
    traditions_and_rituals: List[str]
    what_to_expect: str
    visitor_etiquette: List[str]
    dress_code: Optional[str]
    best_way_to_participate: str
    local_perspective: str
    practical_info: dict


@router.get("/destination/{destination_id}", response_model=List[CulturalEventResponse])
async def list_cultural_events(
    destination_id: str,
    upcoming_only: bool = True,
    event_type: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """List cultural events for a destination"""
    query = select(CulturalEvent).where(CulturalEvent.destination_id == destination_id)
    
    if upcoming_only:
        query = query.where(CulturalEvent.start_date >= datetime.utcnow())
    
    if event_type:
        query = query.where(CulturalEvent.event_type == event_type)
    
    query = query.order_by(CulturalEvent.start_date.asc()).offset(offset).limit(limit)
    
    result = await db.execute(query)
    events = result.scalars().all()
    
    return [
        CulturalEventResponse(
            id=e.id,
            destination_id=e.destination_id,
            name=e.name,
            description=e.description,
            short_description=e.short_description,
            event_type=e.event_type,
            categories=e.categories,
            start_date=e.start_date.isoformat(),
            end_date=e.end_date.isoformat() if e.end_date else None,
            is_recurring=e.is_recurring,
            recurrence_pattern=e.recurrence_pattern,
            venue_name=e.venue_name,
            venue_address=e.venue_address,
            latitude=e.latitude,
            longitude=e.longitude,
            cultural_significance=e.cultural_significance,
            history=e.history,
            traditions=e.traditions,
            dress_code=e.dress_code,
            etiquette=e.etiquette,
            ticket_required=e.ticket_required,
            ticket_url=e.ticket_url,
            price_range=e.price_range,
            capacity=e.capacity,
            language=e.language,
            accessibility_info=e.accessibility_info,
            photos=e.photos,
            primary_photo=e.primary_photo,
            video_url=e.video_url,
            organizer=e.organizer,
            contact_email=e.contact_email,
            contact_phone=e.contact_phone,
            website=e.website,
            ai_cultural_narrative=e.ai_cultural_narrative,
            ai_visitor_guide=e.ai_visitor_guide,
            ai_what_to_expect=e.ai_what_to_expect,
            created_at=e.created_at.isoformat(),
            updated_at=e.updated_at.isoformat(),
        )
        for e in events
    ]


@router.post("/search/nearby", response_model=List[dict])
async def search_events_nearby(
    lat: float,
    lng: float,
    radius: int = 50000,
    keyword: Optional[str] = None,
    current_user: dict = Depends(get_current_user_firebase),
):
    """Search for cultural events near a location using Google Places"""
    try:
        # Use Google Places to find event venues and cultural centers
        places = await google_places_service.search_nearby(
            lat=lat,
            lng=lng,
            radius=radius,
            included_types=["tourist_attraction", "point_of_interest", "cultural_center", 
                          "performing_arts_theater", "museum", "stadium", "amphitheatre"],
            max_results=20,
        )
        
        # Return venues that might host cultural events
        return [
            {
                "place_id": p.place_id,
                "name": p.name,
                "address": p.formatted_address,
                "location": p.location,
                "types": p.types,
                "rating": p.rating,
            }
            for p in places
        ]
    except Exception as e:
        logger.error("Nearby events search failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to search events")


@router.post("/insight", response_model=EventInsightResponse)
async def generate_event_insight(
    event_name: str,
    destination: str,
    country: str,
    event_type: str,
    date_context: str,
    language: str = "en",
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Generate deep cultural insight for an event"""
    try:
        insight = await gemini_service.generate_cultural_event_insight(
            event_name=event_name,
            destination=destination,
            country=country,
            event_type=event_type,
            date_context=date_context,
            language=language,
        )
        
        return EventInsightResponse(
            event_name=insight.event_name,
            cultural_significance=insight.cultural_significance,
            history_and_origins=insight.history_and_origins,
            traditions_and_rituals=insight.traditions_and_rituals,
            what_to_expect=insight.what_to_expect,
            visitor_etiquette=insight.visitor_etiquette,
            dress_code=insight.dress_code,
            best_way_to_participate=insight.best_way_to_participate,
            local_perspective=insight.local_perspective,
            practical_info=insight.practical_info,
        )
    except Exception as e:
        logger.error("Event insight failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate event insight")


@router.post("/insight/event/{event_id}", response_model=EventInsightResponse)
async def generate_insight_for_event(
    event_id: str,
    language: str = "en",
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Generate cultural insight for a saved event"""
    result = await db.execute(select(CulturalEvent).where(CulturalEvent.id == event_id))
    event = result.scalar_one_or_none()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    destination_result = await db.execute(select(Destination).where(Destination.id == event.destination_id))
    destination = destination_result.scalar_one_or_none()
    
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    date_context = event.start_date.strftime("%B %d, %Y")
    if event.end_date:
        date_context += f" to {event.end_date.strftime('%B %d, %Y')}"
    
    try:
        insight = await gemini_service.generate_cultural_event_insight(
            event_name=event.name,
            destination=destination.name,
            country=destination.country,
            event_type=event.event_type,
            date_context=date_context,
            language=language,
        )
        
        # Save insight to event
        event.ai_cultural_narrative = insight.cultural_significance
        event.ai_visitor_guide = insight.best_way_to_participate
        event.ai_what_to_expect = insight.what_to_expect
        await db.commit()
        
        return EventInsightResponse(
            event_name=insight.event_name,
            cultural_significance=insight.cultural_significance,
            history_and_origins=insight.history_and_origins,
            traditions_and_rituals=insight.traditions_and_rituals,
            what_to_expect=insight.what_to_expect,
            visitor_etiquette=insight.visitor_etiquette,
            dress_code=insight.dress_code,
            best_way_to_participate=insight.best_way_to_participate,
            local_perspective=insight.local_perspective,
            practical_info=insight.practical_info,
        )
    except Exception as e:
        logger.error("Event insight failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate event insight")