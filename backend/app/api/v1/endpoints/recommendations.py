"""
Recommendations endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List
from pydantic import BaseModel
import structlog

from app.core.security import get_current_user_firebase
from app.models.user import User
from app.models.trip import Trip
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.gemini import gemini_service, DestinationRecommendation

router = APIRouter()
logger = structlog.get_logger()


class RecommendationRequest(BaseModel):
    interests: List[str]
    travel_style: str
    budget_range: str
    group_size: int = 1
    preferred_regions: Optional[List[str]] = None
    trip_duration_days: Optional[int] = None
    pace: str = "moderate"
    accessibility_needs: Optional[List[str]] = None
    dietary_restrictions: Optional[List[str]] = None
    num_recommendations: int = 5


class RecommendationResponse(BaseModel):
    destination_name: str
    country: str
    region: Optional[str]
    city: Optional[str]
    match_score: float
    reasons: List[str]
    best_for: List[str]
    budget_level: str
    best_time_to_visit: str
    cultural_highlights: List[str]
    hidden_gems_suggested: List[str]
    estimated_daily_cost: Optional[dict]


@router.post("/destinations", response_model=List[RecommendationResponse])
async def get_destination_recommendations(
    request: RecommendationRequest,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Get AI-powered personalized destination recommendations"""
    firebase_uid = current_user.get("uid") or current_user.get("firebase_uid")
    
    result = await db.execute(select(User).where(User.firebase_uid == firebase_uid))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    try:
        recommendations = await gemini_service.recommend_destinations(
            user_interests=request.interests,
            travel_style=request.travel_style,
            budget_range=request.budget_range,
            group_size=request.group_size,
            preferred_regions=request.preferred_regions,
            trip_duration_days=request.trip_duration_days,
            pace=request.pace,
            accessibility_needs=request.accessibility_needs,
            dietary_restrictions=request.dietary_restrictions,
            num_recommendations=request.num_recommendations,
        )
        
        return [
            RecommendationResponse(
                destination_name=r.destination_name,
                country=r.country,
                region=r.region,
                city=r.city,
                match_score=r.match_score,
                reasons=r.reasons,
                best_for=r.best_for,
                budget_level=r.budget_level,
                best_time_to_visit=r.best_time_to_visit,
                cultural_highlights=r.cultural_highlights,
                hidden_gems_suggested=r.hidden_gems_suggested,
                estimated_daily_cost=r.estimated_daily_cost,
            )
            for r in recommendations
        ]
    except Exception as e:
        logger.error("Recommendations failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate recommendations")


@router.post("/from-trip/{trip_id}", response_model=List[RecommendationResponse])
async def get_recommendations_from_trip(
    trip_id: str,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Get recommendations based on an existing trip's preferences"""
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
    
    # Parse interests from trip
    interests = []
    if trip.interests:
        import json
        try:
            interests = json.loads(trip.interests)
        except:
            interests = [trip.interests]
    
    travel_style = trip.travel_style or "cultural"
    budget_range = f"{trip.budget_min or 0}-{trip.budget_max or 5000}" if trip.budget_min or trip.budget_max else "mid-range"
    group_size = trip.group_size
    
    try:
        recommendations = await gemini_service.recommend_destinations(
            user_interests=interests,
            travel_style=travel_style,
            budget_range=budget_range,
            group_size=group_size,
            trip_duration_days=None,
            pace=trip.pace or "moderate",
            num_recommendations=5,
        )
        
        return [
            RecommendationResponse(
                destination_name=r.destination_name,
                country=r.country,
                region=r.region,
                city=r.city,
                match_score=r.match_score,
                reasons=r.reasons,
                best_for=r.best_for,
                budget_level=r.budget_level,
                best_time_to_visit=r.best_time_to_visit,
                cultural_highlights=r.cultural_highlights,
                hidden_gems_suggested=r.hidden_gems_suggested,
                estimated_daily_cost=r.estimated_daily_cost,
            )
            for r in recommendations
        ]
    except Exception as e:
        logger.error("Trip-based recommendations failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate recommendations")