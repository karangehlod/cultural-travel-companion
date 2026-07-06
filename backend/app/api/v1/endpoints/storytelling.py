"""
Storytelling endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List
from pydantic import BaseModel
import structlog

from app.core.security import get_current_user_firebase
from app.models.user import User
from app.models.destination import Destination
from app.models.story import Story
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.gemini import gemini_service, CulturalNarrative

router = APIRouter()
logger = structlog.get_logger()


class NarrativeRequest(BaseModel):
    destination_name: str
    country: str
    region: Optional[str] = None
    city: Optional[str] = None
    focus_topics: Optional[List[str]] = None
    length: str = "detailed"
    language: str = "en"


class NarrativeResponse(BaseModel):
    title: str
    summary: str
    full_narrative: str
    key_themes: List[str]
    historical_period: Optional[str]
    cultural_significance: Optional[str]
    local_perspective: Optional[str]


@router.post("/narrative", response_model=NarrativeResponse)
async def generate_cultural_narrative(
    request: NarrativeRequest,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Generate an immersive cultural narrative for a destination"""
    try:
        narrative = await gemini_service.generate_cultural_narrative(
            destination_name=request.destination_name,
            country=request.country,
            region=request.region,
            city=request.city,
            focus_topics=request.focus_topics,
            length=request.length,
            language=request.language,
        )
        
        return NarrativeResponse(
            title=narrative.title,
            summary=narrative.summary,
            full_narrative=narrative.full_narrative,
            key_themes=narrative.key_themes,
            historical_period=narrative.historical_period,
            cultural_significance=narrative.cultural_significance,
            local_perspective=narrative.local_perspective,
        )
    except Exception as e:
        logger.error("Narrative generation failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate cultural narrative")


@router.post("/narrative/destination/{destination_id}", response_model=NarrativeResponse)
async def generate_narrative_for_destination(
    destination_id: str,
    focus_topics: Optional[List[str]] = None,
    length: str = "detailed",
    language: str = "en",
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Generate cultural narrative for a saved destination"""
    result = await db.execute(select(Destination).where(Destination.id == destination_id))
    destination = result.scalar_one_or_none()
    
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    try:
        narrative = await gemini_service.generate_cultural_narrative(
            destination_name=destination.name,
            country=destination.country,
            region=destination.region,
            city=destination.city,
            focus_topics=focus_topics,
            length=length,
            language=language,
        )
        
        # Save to destination
        destination.ai_cultural_narrative = narrative.full_narrative
        destination.ai_summary = narrative.summary
        await db.commit()
        
        return NarrativeResponse(
            title=narrative.title,
            summary=narrative.summary,
            full_narrative=narrative.full_narrative,
            key_themes=narrative.key_themes,
            historical_period=narrative.historical_period,
            cultural_significance=narrative.cultural_significance,
            local_perspective=narrative.local_perspective,
        )
    except Exception as e:
        logger.error("Destination narrative failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate narrative")


@router.get("/stories/destination/{destination_id}")
async def get_destination_stories(
    destination_id: str,
    story_type: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Get cultural stories for a destination"""
    query = select(Story).where(Story.destination_id == destination_id)
    
    if story_type:
        query = query.where(Story.story_type == story_type)
    
    query = query.order_by(Story.created_at.desc()).offset(offset).limit(limit)
    
    result = await db.execute(query)
    stories = result.scalars().all()
    
    return [
        {
            "id": s.id,
            "title": s.title,
            "content": s.content,
            "summary": s.summary,
            "story_type": s.story_type,
            "categories": s.categories,
            "culture_of_origin": s.culture_of_origin,
            "language_of_origin": s.language_of_origin,
            "historical_period": s.historical_period,
            "cultural_significance": s.cultural_significance,
            "source": s.source,
            "source_type": s.source_type,
            "collected_by": s.collected_by,
            "audio_url": s.audio_url,
            "video_url": s.video_url,
            "photos": s.photos,
            "ai_generated": s.ai_generated,
            "ai_model": s.ai_model,
            "created_at": s.created_at.isoformat(),
        }
        for s in stories
    ]


@router.post("/stories/generate", response_model=NarrativeResponse)
async def generate_cultural_story(
    destination_id: str,
    story_type: str = "legend",  # legend, history, folklore, personal, oral_history, myth
    focus: Optional[str] = None,
    language: str = "en",
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Generate an AI cultural story for a destination"""
    result = await db.execute(select(Destination).where(Destination.id == destination_id))
    destination = result.scalar_one_or_none()
    
    if not destination:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    # Generate story using narrative with specific focus
    focus_topics = [story_type]
    if focus:
        focus_topics.append(focus)
    
    try:
        narrative = await gemini_service.generate_cultural_narrative(
            destination_name=destination.name,
            country=destination.country,
            region=destination.region,
            city=destination.city,
            focus_topics=focus_topics,
            length="detailed",
            language=language,
        )
        
        # Save as story
        story = Story(
            destination_id=destination.id,
            title=narrative.title,
            content=narrative.full_narrative,
            summary=narrative.summary,
            story_type=story_type,
            categories=focus_topics,
            culture_of_origin=destination.country,
            cultural_significance=narrative.cultural_significance,
            ai_generated=True,
            ai_model=settings.GEMINI_MODEL,
        )
        db.add(story)
        await db.commit()
        await db.refresh(story)
        
        return NarrativeResponse(
            title=narrative.title,
            summary=narrative.summary,
            full_narrative=narrative.full_narrative,
            key_themes=narrative.key_themes,
            historical_period=narrative.historical_period,
            cultural_significance=narrative.cultural_significance,
            local_perspective=narrative.local_perspective,
        )
    except Exception as e:
        logger.error("Story generation failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate story")