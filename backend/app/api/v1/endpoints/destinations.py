"""
Destinations endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel
import structlog

from app.core.security import get_current_user_firebase, get_current_user_optional
from app.models.destination import Destination
from app.models.user import User
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from app.services.google_places import google_places_service, PlaceSearchResult
from app.services.google_maps import google_maps_service
from app.services.gemini import gemini_service

router = APIRouter()
logger = structlog.get_logger()


class DestinationSearchRequest(BaseModel):
    query: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    radius: int = 10000
    categories: Optional[List[str]] = None
    cultural_focus: bool = False


class DestinationResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    short_description: Optional[str]
    country: str
    region: Optional[str]
    city: Optional[str]
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    categories: Optional[str]
    place_types: Optional[str]
    cultural_significance: Optional[str]
    unesco_heritage: bool
    primary_photo: Optional[str]
    photos: Optional[str]
    opening_hours: Optional[str]
    website: Optional[str]
    phone: Optional[str]
    rating: Optional[float]
    review_count: Optional[int]
    price_level: Optional[int]
    historical_context: Optional[str]
    cultural_stories: Optional[str]
    local_tips: Optional[str]
    best_time_to_visit: Optional[str]
    ai_summary: Optional[str]
    ai_cultural_narrative: Optional[str]
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


class PlaceSearchResponse(BaseModel):
    place_id: str
    name: str
    formatted_address: str
    location: dict
    types: List[str]
    rating: Optional[float]
    user_ratings_total: Optional[int]
    price_level: Optional[int]
    photos: Optional[List[dict]]
    opening_hours: Optional[dict]
    website: Optional[str]
    phone: Optional[str]
    editorial_summary: Optional[str]


@router.get("/search", response_model=List[PlaceSearchResponse])
async def search_destinations(
    q: str = Query(..., description="Search query"),
    lat: Optional[float] = Query(None, description="Latitude for location bias"),
    lng: Optional[float] = Query(None, description="Longitude for location bias"),
    radius: int = Query(10000, description="Search radius in meters"),
    categories: Optional[str] = Query(None, description="Comma-separated place types"),
    max_results: int = Query(20, description="Maximum results"),
    current_user: Optional[dict] = Depends(get_current_user_optional),
):
    """Search destinations using Google Places API"""
    try:
        included_types = categories.split(",") if categories else None
        
        places = await google_places_service.search_text(
            text_query=q,
            lat=lat,
            lng=lng,
            radius=radius,
            included_types=included_types,
            max_results=max_results,
        )
        
        return [
            PlaceSearchResponse(
                place_id=p.place_id,
                name=p.name,
                formatted_address=p.formatted_address,
                location=p.location,
                types=p.types,
                rating=p.rating,
                user_ratings_total=p.user_ratings_total,
                price_level=p.price_level,
                photos=p.photos,
                opening_hours=p.opening_hours,
                website=p.website,
                phone=p.phone,
                editorial_summary=p.editorial_summary,
            )
            for p in places
        ]
    except Exception as e:
        logger.error("Destination search failed", error=str(e))
        raise HTTPException(status_code=500, detail="Search failed")


@router.get("/nearby", response_model=List[PlaceSearchResponse])
async def nearby_destinations(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    radius: int = Query(5000, description="Search radius in meters"),
    categories: Optional[str] = Query(None, description="Comma-separated place types"),
    cultural_only: bool = Query(False, description="Only cultural places"),
    max_results: int = Query(30, description="Maximum results"),
    current_user: Optional[dict] = Depends(get_current_user_optional),
):
    """Find destinations near a location"""
    try:
        if cultural_only:
            places = await google_places_service.search_cultural_places(
                lat=lat, lng=lng, radius=radius
            )
        else:
            included_types = categories.split(",") if categories else None
            places = await google_places_service.search_nearby(
                lat=lat, lng=lng, radius=radius,
                included_types=included_types, max_results=max_results
            )
        
        return [
            PlaceSearchResponse(
                place_id=p.place_id,
                name=p.name,
                formatted_address=p.formatted_address,
                location=p.location,
                types=p.types,
                rating=p.rating,
                user_ratings_total=p.user_ratings_total,
                price_level=p.price_level,
                photos=p.photos,
                opening_hours=p.opening_hours,
                website=p.website,
                phone=p.phone,
                editorial_summary=p.editorial_summary,
            )
            for p in places
        ]
    except Exception as e:
        logger.error("Nearby search failed", error=str(e))
        raise HTTPException(status_code=500, detail="Nearby search failed")


@router.get("/{place_id}/details", response_model=dict)
async def get_place_details(
    place_id: str,
    current_user: Optional[dict] = Depends(get_current_user_optional),
):
    """Get detailed place information"""
    try:
        details = await google_places_service.get_place_details(place_id)
        return details.model_dump()
    except Exception as e:
        logger.error("Place details failed", place_id=place_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get place details")


@router.get("/{place_id}/photos", response_model=List[dict])
async def get_place_photos(
    place_id: str,
    max_photos: int = Query(10, description="Maximum photos"),
    current_user: Optional[dict] = Depends(get_current_user_optional),
):
    """Get place photos"""
    try:
        photos = await google_places_service.get_place_photos(place_id, max_photos)
        return photos
    except Exception as e:
        logger.error("Place photos failed", place_id=place_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get photos")


@router.post("/{place_id}/generate-narrative", response_model=dict)
async def generate_cultural_narrative(
    place_id: str,
    destination_name: str,
    destination_country: str,
    destination_city: Optional[str] = None,
    language: str = "en",
    current_user: dict = Depends(get_current_user_firebase),
):
    """Generate AI cultural narrative for a destination"""
    try:
        narrative = await gemini_service.generate_cultural_narrative(
            destination_name=destination_name,
            destination_country=destination_country,
            destination_city=destination_city,
            language=language,
        )
        return narrative.model_dump()
    except Exception as e:
        logger.error("Narrative generation failed", place_id=place_id, error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate narrative")


@router.get("/", response_model=List[DestinationResponse])
async def list_destinations(
    country: Optional[str] = Query(None),
    city: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    unesco_only: bool = Query(False),
    limit: int = Query(20, le=100),
    offset: int = Query(0),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[dict] = Depends(get_current_user_optional),
):
    """List saved destinations"""
    query = select(Destination)
    
    if country:
        query = query.where(Destination.country.ilike(f"%{country}%"))
    if city:
        query = query.where(Destination.city.ilike(f"%{city}%"))
    if category:
        query = query.where(Destination.categories.ilike(f"%{category}%"))
    if unesco_only:
        query = query.where(Destination.unesco_heritage == True)
    
    query = query.order_by(Destination.created_at.desc()).offset(offset).limit(limit)
    
    result = await db.execute(query)
    destinations = result.scalars().all()
    
    return [
        DestinationResponse(
            id=d.id,
            name=d.name,
            description=d.description,
            short_description=d.short_description,
            country=d.country,
            region=d.region,
            city=d.city,
            address=d.address,
            latitude=d.latitude,
            longitude=d.longitude,
            categories=d.categories,
            place_types=d.place_types,
            cultural_significance=d.cultural_significance,
            unesco_heritage=d.unesco_heritage,
            primary_photo=d.primary_photo,
            photos=d.photos,
            opening_hours=d.opening_hours,
            website=d.website,
            phone=d.phone,
            rating=d.rating,
            review_count=d.review_count,
            price_level=d.price_level,
            historical_context=d.historical_context,
            cultural_stories=d.cultural_stories,
            local_tips=d.local_tips,
            best_time_to_visit=d.best_time_to_visit,
            ai_summary=d.ai_summary,
            ai_cultural_narrative=d.ai_cultural_narrative,
            created_at=d.created_at.isoformat(),
            updated_at=d.updated_at.isoformat(),
        )
        for d in destinations
    ]


@router.post("/save", response_model=DestinationResponse)
async def save_destination(
    place_id: str,
    name: str,
    country: str,
    city: Optional[str] = None,
    region: Optional[str] = None,
    notes: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user_firebase),
):
    """Save a destination to user's list"""
    firebase_uid = current_user.get("uid") or current_user.get("firebase_uid")
    
    result = await db.execute(select(User).where(User.firebase_uid == firebase_uid))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if already saved
    from app.models.user import user_saved_destinations
    from sqlalchemy import insert
    
    existing = await db.execute(
        select(user_saved_destinations).where(
            user_saved_destinations.c.user_id == user.id,
            user_saved_destinations.c.destination_id == place_id
        )
    )
    if existing.first():
        raise HTTPException(status_code=409, detail="Destination already saved")
    
    # Get or create destination
    result = await db.execute(select(Destination).where(Destination.google_place_id == place_id))
    destination = result.scalar_one_or_none()
    
    if not destination:
        # Fetch details from Google Places
        try:
            details = await google_places_service.get_place_details(place_id)
            
            destination = Destination(
                google_place_id=place_id,
                name=details.name,
                description=details.editorial_summary,
                short_description=details.editorial_summary[:500] if details.editorial_summary else None,
                country=country,
                region=region,
                city=city,
                formatted_address=details.formatted_address,
                latitude=details.location["lat"],
                longitude=details.location["lng"],
                types=details.types,
                rating=details.rating,
                user_ratings_total=details.user_ratings_total,
                price_level=details.price_level,
                photos=details.photos,
                primary_photo=details.photos[0]["name"] if details.photos else None,
                opening_hours=details.opening_hours,
                website=details.website,
                phone=details.phone,
            )
            db.add(destination)
            await db.flush()
        except Exception as e:
            logger.error("Failed to fetch place details", place_id=place_id, error=str(e))
            raise HTTPException(status_code=500, detail="Failed to save destination")
    
    # Save association
    await db.execute(
        insert(user_saved_destinations).values(
            user_id=user.id,
            destination_id=destination.id,
            notes=notes
        )
    )
    await db.commit()
    await db.refresh(destination)
    
    return DestinationResponse(
        id=destination.id,
        name=destination.name,
        description=destination.description,
        short_description=destination.short_description,
        country=destination.country,
        region=destination.region,
        city=destination.city,
        address=destination.address,
        latitude=destination.latitude,
        longitude=destination.longitude,
        categories=destination.categories,
        place_types=destination.place_types,
        cultural_significance=destination.cultural_significance,
        unesco_heritage=destination.unesco_heritage,
        primary_photo=destination.primary_photo,
        photos=destination.photos,
        opening_hours=destination.opening_hours,
        website=destination.website,
        phone=destination.phone,
        rating=destination.rating,
        review_count=destination.review_count,
        price_level=destination.price_level,
        historical_context=destination.historical_context,
        cultural_stories=destination.cultural_stories,
        local_tips=destination.local_tips,
        best_time_to_visit=destination.best_time_to_visit,
        ai_summary=destination.ai_summary,
        ai_cultural_narrative=destination.ai_cultural_narrative,
        created_at=destination.created_at.isoformat(),
        updated_at=destination.updated_at.isoformat(),
    )