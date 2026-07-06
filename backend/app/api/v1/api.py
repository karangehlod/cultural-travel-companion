"""
API router
"""
from fastapi import APIRouter

from app.api.v1.endpoints import trips, destinations, recommendations, storytelling, hidden_gems, cultural_events, cuisine, experiences, itineraries, chat, users, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(trips.router, prefix="/trips", tags=["trips"])
api_router.include_router(destinations.router, prefix="/destinations", tags=["destinations"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(storytelling.router, prefix="/storytelling", tags=["storytelling"])
api_router.include_router(hidden_gems.router, prefix="/hidden-gems", tags=["hidden-gems"])
api_router.include_router(cultural_events.router, prefix="/cultural-events", tags=["cultural-events"])
api_router.include_router(cuisine.router, prefix="/cuisine", tags=["cuisine"])
api_router.include_router(experiences.router, prefix="/experiences", tags=["experiences"])
api_router.include_router(itineraries.router, prefix="/itineraries", tags=["itineraries"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])