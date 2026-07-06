"""
Itineraries endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
import structlog
import json

from app.core.security import get_current_user_firebase
from app.models.user import User
from app.models.trip import Trip, TripStatus
from app.models.itinerary import ItineraryDay, ItineraryItem
from app.models.destination import Destination
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.gemini import gemini_service, FullItinerary, ItineraryDay as AIDay

router = APIRouter()
logger = structlog.get_logger()


class ItineraryGenerationRequest(BaseModel):
    destination: str
    country: str
    duration_days: int
    travel_style: str
    budget_range: str
    group_size: int
    interests: List[str]
    pace: str = "moderate"
    start_date: Optional[str] = None
    special_requirements: Optional[str] = None


class ItineraryDayResponse(BaseModel):
    id: str
    trip_id: str
    day_number: int
    date: Optional[str]
    title: Optional[str]
    theme: Optional[str]
    notes: Optional[str]
    ai_day_narrative: Optional[str]
    ai_cultural_insights: Optional[str]
    items: List[dict] = []
    
    class Config:
        from_attributes = True


class ItineraryResponse(BaseModel):
    trip_title: str
    destination: str
    duration_days: int
    travel_style: str
    budget_range: str
    group_size: int
    overview: str
    cultural_context: str
    days: List[AIDay]
    practical_tips: List[str]
    packing_suggestions: List[str]
    cultural_etiquette: List[str]
    emergency_info: dict


@router.post("/generate", response_model=ItineraryResponse)
async def generate_itinerary(
    request: ItineraryGenerationRequest,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Generate a complete AI cultural itinerary"""
    try:
        itinerary = await gemini_service.generate_itinerary(
            destination=request.destination,
            country=request.country,
            duration_days=request.duration_days,
            travel_style=request.travel_style,
            budget_range=request.budget_range,
            group_size=request.group_size,
            interests=request.interests,
            pace=request.pace,
            start_date=request.start_date,
            special_requirements=request.special_requirements,
        )
        
        return ItineraryResponse(
            trip_title=itinerary.trip_title,
            destination=itinerary.destination,
            duration_days=itinerary.duration_days,
            travel_style=itinerary.travel_style,
            budget_range=itinerary.budget_range,
            group_size=itinerary.group_size,
            overview=itinerary.overview,
            cultural_context=itinerary.cultural_context,
            days=itinerary.days,
            practical_tips=itinerary.practical_tips,
            packing_suggestions=itinerary.packing_suggestions,
            cultural_etiquette=itinerary.cultural_etiquette,
            emergency_info=itinerary.emergency_info,
        )
    except Exception as e:
        logger.error("Itinerary generation failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate itinerary")


@router.post("/generate/trip/{trip_id}", response_model=ItineraryResponse)
async def generate_itinerary_for_trip(
    trip_id: str,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Generate itinerary based on trip preferences"""
    firebase_uid = current_user.get("uid") or current_user.get("firebase_uid")
    
    result = await db.execute(select(User).where(User.firebase_uid == firebase_uid))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = await db.execute(
        select(Trip).where(Trip.id == trip_id, Trip.user_id == user.id)
    )
    trip = result.scalar_one_or_none()
    
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Parse interests
    interests = []
    if trip.interests:
        try:
            interests = json.loads(trip.interests)
        except:
            interests = [trip.interests]
    
    destination = trip.destination_city or trip.destination_region or trip.destination_country
    country = trip.destination_country
    
    if not destination or not country:
        raise HTTPException(status_code=400, detail="Trip missing destination info")
    
    # Calculate duration
    duration_days = 7
    if trip.start_date and trip.end_date:
        duration_days = (trip.end_date - trip.start_date).days + 1
    
    try:
        itinerary = await gemini_service.generate_itinerary(
            destination=destination,
            country=country,
            duration_days=duration_days,
            travel_style=trip.travel_style or "cultural",
            budget_range=f"${trip.budget_min or 0}-${trip.budget_max or 5000}" if trip.budget_min or trip.budget_max else "mid-range",
            group_size=trip.group_size,
            interests=interests,
            pace=trip.pace or "moderate",
            start_date=trip.start_date.isoformat() if trip.start_date else None,
        )
        
        # Save AI-generated itinerary to trip
        trip.ai_generated_itinerary = json.dumps({
            "overview": itinerary.overview,
            "cultural_context": itinerary.cultural_context,
            "days": [day.model_dump() for day in itinerary.days],
            "practical_tips": itinerary.practical_tips,
            "packing_suggestions": itinerary.packing_suggestions,
            "cultural_etiquette": itinerary.cultural_etiquette,
            "emergency_info": itinerary.emergency_info,
        })
        
        # Create itinerary days in database
        for ai_day in itinerary.days:
            day = ItineraryDay(
                trip_id=trip.id,
                day_number=ai_day.day_number,
                date=datetime.fromisoformat(ai_day.date) if ai_day.date else None,
                title=ai_day.title,
                theme=ai_day.theme,
                ai_day_narrative=ai_day.narrative,
                ai_cultural_insights="\n".join(ai_day.cultural_insights),
            )
            db.add(day)
            await db.flush()
            
            for activity in ai_day.activities:
                item = ItineraryItem(
                    day_id=day.id,
                    item_type=activity.get("type", "destination"),
                    title=activity.get("title", ""),
                    description=activity.get("description"),
                    start_time=activity.get("time"),
                    duration_minutes=activity.get("duration_minutes"),
                    address=activity.get("location"),
                    place_name=activity.get("location"),
                    estimated_cost=activity.get("cost_estimate_usd"),
                    ai_context=activity.get("cultural_context"),
                    ai_cultural_tips=activity.get("cultural_etiquette"),
                    sort_order=ai_day.activities.index(activity),
                )
                db.add(item)
        
        trip.status = TripStatus.PLANNING
        await db.commit()
        
        return ItineraryResponse(
            trip_title=itinerary.trip_title,
            destination=itinerary.destination,
            duration_days=itinerary.duration_days,
            travel_style=itinerary.travel_style,
            budget_range=itinerary.budget_range,
            group_size=itinerary.group_size,
            overview=itinerary.overview,
            cultural_context=itinerary.cultural_context,
            days=itinerary.days,
            practical_tips=itinerary.practical_tips,
            packing_suggestions=itinerary.packing_suggestions,
            cultural_etiquette=itinerary.cultural_etiquette,
            emergency_info=itinerary.emergency_info,
        )
    except Exception as e:
        logger.error("Trip itinerary generation failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate itinerary")


@router.get("/trip/{trip_id}", response_model=List[ItineraryDayResponse])
async def get_trip_itinerary(
    trip_id: str,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Get itinerary for a trip"""
    firebase_uid = current_user.get("uid") or current_user.get("firebase_uid")
    
    result = await db.execute(select(User).where(User.firebase_uid == firebase_uid))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = await db.execute(
        select(Trip).where(Trip.id == trip_id, Trip.user_id == user.id)
    )
    trip = result.scalar_one_or_none()
    
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    result = await db.execute(
        select(ItineraryDay)
        .where(ItineraryDay.trip_id == trip.id)
        .order_by(ItineraryDay.day_number)
    )
    days = result.scalars().all()
    
    itinerary_days = []
    for day in days:
        result = await db.execute(
            select(ItineraryItem)
            .where(ItineraryItem.day_id == day.id)
            .order_by(ItineraryItem.sort_order, ItineraryItem.start_time)
        )
        items = result.scalars().all()
        
        itinerary_days.append(ItineraryDayResponse(
            id=day.id,
            trip_id=day.trip_id,
            day_number=day.day_number,
            date=day.date.isoformat() if day.date else None,
            title=day.title,
            theme=day.theme,
            notes=day.notes,
            ai_day_narrative=day.ai_day_narrative,
            ai_cultural_insights=day.ai_cultural_insights,
            items=[
                {
                    "id": item.id,
                    "item_type": item.item_type,
                    "title": item.title,
                    "description": item.description,
                    "start_time": item.start_time,
                    "end_time": item.end_time,
                    "duration_minutes": item.duration_minutes,
                    "address": item.address,
                    "latitude": item.latitude,
                    "longitude": item.longitude,
                    "place_name": item.place_name,
                    "estimated_cost": item.estimated_cost,
                    "currency": item.currency,
                    "transport_mode": item.transport_mode,
                    "transport_details": item.transport_details,
                    "transport_duration_minutes": item.transport_duration_minutes,
                    "transport_cost": item.transport_cost,
                    "ai_context": item.ai_context,
                    "ai_cultural_tips": item.ai_cultural_tips,
                    "sort_order": item.sort_order,
                }
                for item in items
            ],
        ))
    
    return itinerary_days


@router.post("/trip/{trip_id}/day", response_model=ItineraryDayResponse)
async def add_itinerary_day(
    trip_id: str,
    day_number: int,
    date: Optional[str] = None,
    title: Optional[str] = None,
    theme: Optional[str] = None,
    notes: Optional[str] = None,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Add a day to trip itinerary"""
    firebase_uid = current_user.get("uid") or current_user.get("firebase_uid")
    
    result = await db.execute(select(User).where(User.firebase_uid == firebase_uid))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = await db.execute(
        select(Trip).where(Trip.id == trip_id, Trip.user_id == user.id)
    )
    trip = result.scalar_one_or_none()
    
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    day = ItineraryDay(
        trip_id=trip.id,
        day_number=day_number,
        date=datetime.fromisoformat(date) if date else None,
        title=title,
        theme=theme,
        notes=notes,
    )
    
    db.add(day)
    await db.commit()
    await db.refresh(day)
    
    return ItineraryDayResponse(
        id=day.id,
        trip_id=day.trip_id,
        day_number=day.day_number,
        date=day.date.isoformat() if day.date else None,
        title=day.title,
        theme=day.theme,
        notes=day.notes,
        ai_day_narrative=day.ai_day_narrative,
        ai_cultural_insights=day.ai_cultural_insights,
        items=[],
    )


@router.post("/trip/{trip_id}/day/{day_id}/item", response_model=dict)
async def add_itinerary_item(
    trip_id: str,
    day_id: str,
    item_type: str,
    title: str,
    description: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    duration_minutes: Optional[int] = None,
    address: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    place_name: Optional[str] = None,
    estimated_cost: Optional[float] = None,
    currency: str = "USD",
    transport_mode: Optional[str] = None,
    transport_details: Optional[str] = None,
    transport_duration_minutes: Optional[int] = None,
    transport_cost: Optional[float] = None,
    ai_context: Optional[str] = None,
    ai_cultural_tips: Optional[str] = None,
    sort_order: int = 0,
    destination_id: Optional[str] = None,
    experience_id: Optional[str] = None,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Add an item to itinerary day"""
    firebase_uid = current_user.get("uid") or current_user.get("firebase_uid")
    
    result = await db.execute(select(User).where(User.firebase_uid == firebase_uid))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = await db.execute(
        select(Trip).where(Trip.id == trip_id, Trip.user_id == user.id)
    )
    trip = result.scalar_one_or_none()
    
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    result = await db.execute(
        select(ItineraryDay).where(ItineraryDay.id == day_id, ItineraryDay.trip_id == trip.id)
    )
    day = result.scalar_one_or_none()
    
    if not day:
        raise HTTPException(status_code=404, detail="Day not found")
    
    item = ItineraryItem(
        day_id=day.id,
        item_type=item_type,
        title=title,
        description=description,
        start_time=start_time,
        end_time=end_time,
        duration_minutes=duration_minutes,
        address=address,
        latitude=latitude,
        longitude=longitude,
        place_name=place_name,
        estimated_cost=estimated_cost,
        currency=currency,
        transport_mode=transport_mode,
        transport_details=transport_details,
        transport_duration_minutes=transport_duration_minutes,
        transport_cost=transport_cost,
        ai_context=ai_context,
        ai_cultural_tips=ai_cultural_tips,
        sort_order=sort_order,
        destination_id=destination_id,
        experience_id=experience_id,
    )
    
    db.add(item)
    await db.commit()
    await db.refresh(item)
    
    return {
        "id": item.id,
        "day_id": item.day_id,
        "item_type": item.item_type,
        "title": item.title,
        "description": item.description,
        "start_time": item.start_time,
        "end_time": item.end_time,
        "duration_minutes": item.duration_minutes,
        "address": item.address,
        "latitude": item.latitude,
        "longitude": item.longitude,
        "place_name": item.place_name,
        "estimated_cost": item.estimated_cost,
        "currency": item.currency,
        "transport_mode": item.transport_mode,
        "transport_details": item.transport_details,
        "transport_duration_minutes": item.transport_duration_minutes,
        "transport_cost": item.transport_cost,
        "ai_context": item.ai_context,
        "ai_cultural_tips": item.ai_cultural_tips,
        "sort_order": item.sort_order,
    }