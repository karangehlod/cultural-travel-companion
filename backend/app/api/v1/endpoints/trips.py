"""
Trips endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import structlog

from app.core.security import get_current_user_firebase
from app.models.trip import Trip, TripStatus
from app.models.itinerary import ItineraryDay, ItineraryItem
from app.models.user import User
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter()
logger = structlog.get_logger()


class TripCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    destination_country: Optional[str] = None
    destination_city: Optional[str] = None
    destination_region: Optional[str] = None
    destination_coordinates: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    currency: str = "USD"
    travel_style: Optional[str] = None
    interests: Optional[str] = None
    group_size: int = 1
    pace: Optional[str] = None


class TripUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    destination_country: Optional[str] = None
    destination_city: Optional[str] = None
    destination_region: Optional[str] = None
    destination_coordinates: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    currency: Optional[str] = None
    travel_style: Optional[str] = None
    interests: Optional[str] = None
    group_size: Optional[int] = None
    pace: Optional[str] = None
    status: Optional[TripStatus] = None


class TripResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str]
    status: str
    start_date: Optional[str]
    end_date: Optional[str]
    destination_country: Optional[str]
    destination_city: Optional[str]
    destination_region: Optional[str]
    destination_coordinates: Optional[str]
    budget_min: Optional[float]
    budget_max: Optional[float]
    currency: str
    travel_style: Optional[str]
    interests: Optional[str]
    group_size: int
    pace: Optional[str]
    created_at: str
    updated_at: str
    confirmed_at: Optional[str]
    
    class Config:
        from_attributes = True


class ItineraryItemResponse(BaseModel):
    id: str
    day_id: str
    item_type: str
    title: str
    description: Optional[str]
    start_time: Optional[str]
    end_time: Optional[str]
    duration_minutes: Optional[int]
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    place_name: Optional[str]
    estimated_cost: Optional[float]
    currency: str
    transport_mode: Optional[str]
    transport_details: Optional[str]
    transport_duration_minutes: Optional[int]
    transport_cost: Optional[float]
    ai_context: Optional[str]
    ai_cultural_tips: Optional[str]
    sort_order: int
    
    class Config:
        from_attributes = True


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
    items: List[ItineraryItemResponse] = []
    
    class Config:
        from_attributes = True


class TripDetailResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: Optional[str]
    status: str
    start_date: Optional[str]
    end_date: Optional[str]
    destination_country: Optional[str]
    destination_city: Optional[str]
    destination_region: Optional[str]
    destination_coordinates: Optional[str]
    budget_min: Optional[float]
    budget_max: Optional[float]
    currency: str
    travel_style: Optional[str]
    interests: Optional[str]
    group_size: int
    pace: Optional[str]
    ai_generated_itinerary: Optional[str]
    ai_cultural_insights: Optional[str]
    ai_recommendations: Optional[str]
    created_at: str
    updated_at: str
    confirmed_at: Optional[str]
    itinerary_days: List[ItineraryDayResponse] = []
    
    class Config:
        from_attributes = True


@router.post("/", response_model=TripResponse, status_code=201)
async def create_trip(
    trip_data: TripCreate,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Create a new trip"""
    firebase_uid = current_user.get("uid") or current_user.get("firebase_uid")
    
    result = await db.execute(select(User).where(User.firebase_uid == firebase_uid))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    trip = Trip(
        user_id=user.id,
        **trip_data.model_dump()
    )
    
    db.add(trip)
    await db.commit()
    await db.refresh(trip)
    
    logger.info("Trip created", trip_id=trip.id, user_id=user.id)
    
    return TripResponse(
        id=trip.id,
        user_id=trip.user_id,
        title=trip.title,
        description=trip.description,
        status=trip.status.value,
        start_date=trip.start_date.isoformat() if trip.start_date else None,
        end_date=trip.end_date.isoformat() if trip.end_date else None,
        destination_country=trip.destination_country,
        destination_city=trip.destination_city,
        destination_region=trip.destination_region,
        destination_coordinates=trip.destination_coordinates,
        budget_min=trip.budget_min,
        budget_max=trip.budget_max,
        currency=trip.currency,
        travel_style=trip.travel_style,
        interests=trip.interests,
        group_size=trip.group_size,
        pace=trip.pace,
        created_at=trip.created_at.isoformat(),
        updated_at=trip.updated_at.isoformat(),
        confirmed_at=trip.confirmed_at.isoformat() if trip.confirmed_at else None,
    )


@router.get("/", response_model=List[TripResponse])
async def list_trips(
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """List user's trips"""
    firebase_uid = current_user.get("uid") or current_user.get("firebase_uid")
    
    result = await db.execute(select(User).where(User.firebase_uid == firebase_uid))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = await db.execute(
        select(Trip).where(Trip.user_id == user.id).order_by(Trip.created_at.desc())
    )
    trips = result.scalars().all()
    
    return [
        TripResponse(
            id=t.id,
            user_id=t.user_id,
            title=t.title,
            description=t.description,
            status=t.status.value,
            start_date=t.start_date.isoformat() if t.start_date else None,
            end_date=t.end_date.isoformat() if t.end_date else None,
            destination_country=t.destination_country,
            destination_city=t.destination_city,
            destination_region=t.destination_region,
            destination_coordinates=t.destination_coordinates,
            budget_min=t.budget_min,
            budget_max=t.budget_max,
            currency=t.currency,
            travel_style=t.travel_style,
            interests=t.interests,
            group_size=t.group_size,
            pace=t.pace,
            created_at=t.created_at.isoformat(),
            updated_at=t.updated_at.isoformat(),
            confirmed_at=t.confirmed_at.isoformat() if t.confirmed_at else None,
        )
        for t in trips
    ]


@router.get("/{trip_id}", response_model=TripDetailResponse)
async def get_trip(
    trip_id: str,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Get trip details with itinerary"""
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
    
    # Get itinerary days with items
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
                ItineraryItemResponse(
                    id=item.id,
                    day_id=item.day_id,
                    item_type=item.item_type,
                    title=item.title,
                    description=item.description,
                    start_time=item.start_time,
                    end_time=item.end_time,
                    duration_minutes=item.duration_minutes,
                    address=item.address,
                    latitude=item.latitude,
                    longitude=item.longitude,
                    place_name=item.place_name,
                    estimated_cost=item.estimated_cost,
                    currency=item.currency,
                    transport_mode=item.transport_mode,
                    transport_details=item.transport_details,
                    transport_duration_minutes=item.transport_duration_minutes,
                    transport_cost=item.transport_cost,
                    ai_context=item.ai_context,
                    ai_cultural_tips=item.ai_cultural_tips,
                    sort_order=item.sort_order,
                )
                for item in items
            ],
        ))
    
    return TripDetailResponse(
        id=trip.id,
        user_id=trip.user_id,
        title=trip.title,
        description=trip.description,
        status=trip.status.value,
        start_date=trip.start_date.isoformat() if trip.start_date else None,
        end_date=trip.end_date.isoformat() if trip.end_date else None,
        destination_country=trip.destination_country,
        destination_city=trip.destination_city,
        destination_region=trip.destination_region,
        destination_coordinates=trip.destination_coordinates,
        budget_min=trip.budget_min,
        budget_max=trip.budget_max,
        currency=trip.currency,
        travel_style=trip.travel_style,
        interests=trip.interests,
        group_size=trip.group_size,
        pace=trip.pace,
        ai_generated_itinerary=trip.ai_generated_itinerary,
        ai_cultural_insights=trip.ai_cultural_insights,
        ai_recommendations=trip.ai_recommendations,
        created_at=trip.created_at.isoformat(),
        updated_at=trip.updated_at.isoformat(),
        confirmed_at=trip.confirmed_at.isoformat() if trip.confirmed_at else None,
        itinerary_days=itinerary_days,
    )


@router.patch("/{trip_id}", response_model=TripResponse)
async def update_trip(
    trip_id: str,
    trip_data: TripUpdate,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Update a trip"""
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
    
    update_dict = trip_data.model_dump(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(trip, field, value)
    
    await db.commit()
    await db.refresh(trip)
    
    return TripResponse(
        id=trip.id,
        user_id=trip.user_id,
        title=trip.title,
        description=trip.description,
        status=trip.status.value,
        start_date=trip.start_date.isoformat() if trip.start_date else None,
        end_date=trip.end_date.isoformat() if trip.end_date else None,
        destination_country=trip.destination_country,
        destination_city=trip.destination_city,
        destination_region=trip.destination_region,
        destination_coordinates=trip.destination_coordinates,
        budget_min=trip.budget_min,
        budget_max=trip.budget_max,
        currency=trip.currency,
        travel_style=trip.travel_style,
        interests=trip.interests,
        group_size=trip.group_size,
        pace=trip.pace,
        created_at=trip.created_at.isoformat(),
        updated_at=trip.updated_at.isoformat(),
        confirmed_at=trip.confirmed_at.isoformat() if trip.confirmed_at else None,
    )


@router.delete("/{trip_id}")
async def delete_trip(
    trip_id: str,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Delete a trip"""
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
    
    await db.delete(trip)
    await db.commit()
    
    return {"message": "Trip deleted successfully"}