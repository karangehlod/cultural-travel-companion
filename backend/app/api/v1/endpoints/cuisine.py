"""
Cuisine endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List
from pydantic import BaseModel
import structlog

from app.core.security import get_current_user_firebase
from app.models.user import User
from app.models.destination import Destination
from app.models.cuisine import Cuisine, CuisineType
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.gemini import gemini_service, CuisineInsight
from app.services.google_places import google_places_service

router = APIRouter()
logger = structlog.get_logger()


class CuisineResponse(BaseModel):
    id: str
    destination_id: str
    name: str
    description: str
    short_description: Optional[str]
    cuisine_type: str
    dish_category: Optional[str]
    cultural_significance: Optional[str]
    history: Optional[str]
    region_of_origin: Optional[str]
    traditional_occasion: Optional[str]
    ingredients: Optional[str]
    allergens: Optional[str]
    dietary_tags: Optional[str]
    preparation_method: Optional[str]
    cooking_time_minutes: Optional[int]
    venue_name: Optional[str]
    address: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    price_range: Optional[str]
    price_level: Optional[int]
    photos: Optional[str]
    primary_photo: Optional[str]
    recipe: Optional[str]
    serves: Optional[int]
    ai_cultural_narrative: Optional[str]
    ai_pairing_suggestions: Optional[str]
    ai_local_insights: Optional[str]
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True


class CuisineInsightResponse(BaseModel):
    dish_name: str
    description: str
    cultural_significance: str
    history: str
    region_of_origin: str
    traditional_occasion: str
    key_ingredients: List[str]
    preparation_highlights: str
    flavor_profile: str
    pairing_suggestions: List[str]
    where_to_find_authentic_version: str
    local_eating_customs: List[str]


@router.get("/destination/{destination_id}", response_model=List[CuisineResponse])
async def list_cuisines(
    destination_id: str,
    cuisine_type: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """List cuisines for a destination"""
    query = select(Cuisine).where(Cuisine.destination_id == destination_id)
    
    if cuisine_type:
        query = query.where(Cuisine.cuisine_type == cuisine_type)
    
    query = query.order_by(Cuisine.created_at.desc()).offset(offset).limit(limit)
    
    result = await db.execute(query)
    cuisines = result.scalars().all()
    
    return [
        CuisineResponse(
            id=c.id,
            destination_id=c.destination_id,
            name=c.name,
            description=c.description,
            short_description=c.short_description,
            cuisine_type=c.cuisine_type.value,
            dish_category=c.dish_category,
            cultural_significance=c.cultural_significance,
            history=c.history,
            region_of_origin=c.region_of_origin,
            traditional_occasion=c.traditional_occasion,
            ingredients=c.ingredients,
            allergens=c.allergens,
            dietary_tags=c.dietary_tags,
            preparation_method=c.preparation_method,
            cooking_time_minutes=c.cooking_time_minutes,
            venue_name=c.venue_name,
            address=c.address,
            latitude=c.latitude,
            longitude=c.longitude,
            price_range=c.price_range,
            price_level=c.price_level,
            photos=c.photos,
            primary_photo=c.primary_photo,
            recipe=c.recipe,
            serves=c.serves,
            ai_cultural_narrative=c.ai_cultural_narrative,
            ai_pairing_suggestions=c.ai_pairing_suggestions,
            ai_local_insights=c.ai_local_insights,
            created_at=c.created_at.isoformat(),
            updated_at=c.updated_at.isoformat(),
        )
        for c in cuisines
    ]


@router.get("/search/nearby", response_model=List[dict])
async def search_food_nearby(
    lat: float,
    lng: float,
    radius: int = 5000,
    cuisine_type: Optional[str] = None,
    current_user: dict = Depends(get_current_user_firebase),
):
    """Search for food places near a location"""
    try:
        places = await google_places_service.search_food_places(lat=lat, lng=lng, radius=radius)
        
        return [
            {
                "place_id": p.place_id,
                "name": p.name,
                "address": p.formatted_address,
                "location": p.location,
                "types": p.types,
                "rating": p.rating,
                "price_level": p.price_level,
                "photos": p.photos,
            }
            for p in places
        ]
    except Exception as e:
        logger.error("Food search failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to search food places")


@router.post("/insight", response_model=CuisineInsightResponse)
async def generate_cuisine_insight(
    dish_name: str,
    destination: str,
    country: str,
    cuisine_type: str = "traditional",
    language: str = "en",
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Generate deep cultural insight for a dish/cuisine"""
    try:
        insight = await gemini_service.generate_cuisine_insight(
            dish_name=dish_name,
            destination=destination,
            country=country,
            cuisine_type=cuisine_type,
            language=language,
        )
        
        return CuisineInsightResponse(
            dish_name=insight.dish_name,
            description=insight.description,
            cultural_significance=insight.cultural_significance,
            history=insight.history,
            region_of_origin=insight.region_of_origin,
            traditional_occasion=insight.traditional_occasion,
            key_ingredients=insight.key_ingredients,
            preparation_highlights=insight.preparation_highlights,
            flavor_profile=insight.flavor_profile,
            pairing_suggestions=insight.pairing_suggestions,
            where_to_find_authentic_version=insight.where_to_find_authentic_version,
            local_eating_customs=insight.local_eating_customs,
        )
    except Exception as e:
        logger.error("Cuisine insight failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate cuisine insight")


@router.post("/insight/cuisine/{cuisine_id}", response_model=CuisineInsightResponse)
async def generate_insight_for_cuisine(
    cuisine_id: str,
    language: str = "en",
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Generate cultural insight for a saved cuisine"""
    result = await db.execute(select(Cuisine).where(Cuisine.id == cuisine_id))
    cuisine = result.scalar_one_or_none()
    
    if not cuisine:
        raise HTTPException(status_code=404, detail="Cuisine not found")
    
    destination_result = await db.execute(select(Destination).where(Destination.id == cuisine.destination_id))
    destination = destination_result.scalar_one_or_none()
    
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    try:
        insight = await gemini_service.generate_cuisine_insight(
            dish_name=cuisine.name,
            destination=destination.name,
            country=destination.country,
            cuisine_type=cuisine.cuisine_type.value,
            language=language,
        )
        
        # Save insight to cuisine
        cuisine.ai_cultural_narrative = insight.cultural_significance
        cuisine.ai_pairing_suggestions = insight.pairing_suggestions
        cuisine.ai_local_insights = insight.local_eating_customs
        await db.commit()
        
        return CuisineInsightResponse(
            dish_name=insight.dish_name,
            description=insight.description,
            cultural_significance=insight.cultural_significance,
            history=insight.history,
            region_of_origin=insight.region_of_origin,
            traditional_occasion=insight.traditional_occasion,
            key_ingredients=insight.key_ingredients,
            preparation_highlights=insight.preparation_highlights,
            flavor_profile=insight.flavor_profile,
            pairing_suggestions=insight.pairing_suggestions,
            where_to_find_authentic_version=insight.where_to_find_authentic_version,
            local_eating_customs=insight.local_eating_customs,
        )
    except Exception as e:
        logger.error("Cuisine insight failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate cuisine insight")