"""
Chat endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List
from pydantic import BaseModel
import structlog
import json
from datetime import datetime

from app.core.security import get_current_user_firebase
from app.models.user import User
from app.models.trip import Trip
from app.models.chat import ChatSession, ChatMessage
from app.core.database import get_db
from app.core.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.services.gemini import gemini_service, ChatResponse

router = APIRouter()
logger = structlog.get_logger()


class ChatMessageRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    trip_id: Optional[str] = None


class ChatMessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    tokens_used: Optional[int]
    model: Optional[str]
    created_at: str
    
    class Config:
        from_attributes = True


class ChatSessionResponse(BaseModel):
    id: str
    user_id: str
    trip_id: Optional[str]
    title: Optional[str]
    context: Optional[str]
    created_at: str
    updated_at: str
    last_message_at: Optional[str]
    messages: List[ChatMessageResponse] = []
    
    class Config:
        from_attributes = True


@router.post("/message", response_model=ChatMessageResponse)
async def send_message(
    request: ChatMessageRequest,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Send a message to the AI cultural travel companion"""
    firebase_uid = current_user.get("uid") or current_user.get("firebase_uid")
    
    result = await db.execute(select(User).where(User.firebase_uid == firebase_uid))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get or create chat session
    session = None
    if request.session_id:
        result = await db.execute(
            select(ChatSession).where(ChatSession.id == request.session_id, ChatSession.user_id == user.id)
        )
        session = result.scalar_one_or_none()
        
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
    elif request.trip_id:
        result = await db.execute(
            select(Trip).where(Trip.id == request.trip_id, Trip.user_id == user.id)
        )
        trip = result.scalar_one_or_none()
        
        if not trip:
            raise HTTPException(status_code=404, detail="Trip not found")
        
        # Check for existing session for this trip
        result = await db.execute(
            select(ChatSession).where(ChatSession.trip_id == trip.id, ChatSession.user_id == user.id)
        )
        session = result.scalar_one_or_none()
        
        if not session:
            session = ChatSession(
                user_id=user.id,
                trip_id=trip.id,
                title=f"Chat: {trip.title}",
                context=json.dumps({
                    "destination": trip.destination_city or trip.destination_country,
                    "travel_style": trip.travel_style,
                    "interests": trip.interests,
                    "budget_range": f"{trip.budget_min}-{trip.budget_max}" if trip.budget_min or trip.budget_max else None,
                }),
            )
            db.add(session)
            await db.flush()
    else:
        # Create new general session
        session = ChatSession(
            user_id=user.id,
            title="Cultural Travel Companion",
        )
        db.add(session)
        await db.flush()
    
    # Get conversation history
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session.id)
        .order_by(ChatMessage.created_at.desc())
        .limit(20)
    )
    history = result.scalars().all()
    history = list(reversed(history))
    
    conversation_history = [
        {"role": msg.role, "content": msg.content}
        for msg in history
    ]
    
    # Build trip context
    trip_context = None
    if session.trip_id:
        result = await db.execute(select(Trip).where(Trip.id == session.trip_id))
        trip = result.scalar_one_or_none()
        if trip:
            trip_context = {
                "title": trip.title,
                "destination": f"{trip.destination_city}, {trip.destination_country}" if trip.destination_city else trip.destination_country,
                "dates": f"{trip.start_date} to {trip.end_date}" if trip.start_date and trip.end_date else None,
                "travel_style": trip.travel_style,
                "interests": trip.interests,
                "budget": f"{trip.budget_min}-{trip.budget_max} {trip.currency}" if trip.budget_min or trip.budget_max else None,
                "group_size": trip.group_size,
            }
    
    # Build user profile
    user_profile = {
        "display_name": user.display_name,
        "travel_style": user.travel_style,
        "interests": user.interests,
        "budget_range": user.budget_range,
        "dietary_restrictions": user.dietary_restrictions,
        "accessibility_needs": user.accessibility_needs,
        "preferred_languages": user.preferred_languages,
    }
    
    try:
        # Generate AI response
        response = await gemini_service.chat_with_travel_companion(
            user_message=request.message,
            conversation_history=conversation_history,
            trip_context=trip_context,
            user_profile=user_profile,
        )
        
        # Save user message
        user_msg = ChatMessage(
            session_id=session.id,
            role="user",
            content=request.message,
        )
        db.add(user_msg)
        
        # Save assistant message
        assistant_msg = ChatMessage(
            session_id=session.id,
            role="assistant",
            content=response.content,
            model=settings.GEMINI_MODEL,
        )
        db.add(assistant_msg)
        
        # Update session
        session.last_message_at = datetime.utcnow()
        session.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(assistant_msg)
        
        return ChatMessageResponse(
            id=assistant_msg.id,
            session_id=assistant_msg.session_id,
            role=assistant_msg.role,
            content=assistant_msg.content,
            tokens_used=assistant_msg.tokens_used,
            model=assistant_msg.model,
            created_at=assistant_msg.created_at.isoformat(),
        )
    except Exception as e:
        logger.error("Chat failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to generate response")


@router.get("/sessions", response_model=List[ChatSessionResponse])
async def list_chat_sessions(
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """List user's chat sessions"""
    firebase_uid = current_user.get("uid") or current_user.get("firebase_uid")
    
    result = await db.execute(select(User).where(User.firebase_uid == firebase_uid))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = await db.execute(
        select(ChatSession)
        .where(ChatSession.user_id == user.id)
        .order_by(ChatSession.last_message_at.desc().nullslast())
    )
    sessions = result.scalars().all()
    
    return [
        ChatSessionResponse(
            id=s.id,
            user_id=s.user_id,
            trip_id=s.trip_id,
            title=s.title,
            context=s.context,
            created_at=s.created_at.isoformat(),
            updated_at=s.updated_at.isoformat(),
            last_message_at=s.last_message_at.isoformat() if s.last_message_at else None,
            messages=[],
        )
        for s in sessions
    ]


@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session(
    session_id: str,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Get a chat session with messages"""
    firebase_uid = current_user.get("uid") or current_user.get("firebase_uid")
    
    result = await db.execute(select(User).where(User.firebase_uid == firebase_uid))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = await db.execute(
        select(ChatSession).where(ChatSession.id == session_id, ChatSession.user_id == user.id)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session.id)
        .order_by(ChatMessage.created_at.asc())
    )
    messages = result.scalars().all()
    
    return ChatSessionResponse(
        id=session.id,
        user_id=session.user_id,
        trip_id=session.trip_id,
        title=session.title,
        context=session.context,
        created_at=session.created_at.isoformat(),
        updated_at=session.updated_at.isoformat(),
        last_message_at=session.last_message_at.isoformat() if session.last_message_at else None,
        messages=[
            ChatMessageResponse(
                id=m.id,
                session_id=m.session_id,
                role=m.role,
                content=m.content,
                tokens_used=m.tokens_used,
                model=m.model,
                created_at=m.created_at.isoformat(),
            )
            for m in messages
        ],
    )


@router.delete("/sessions/{session_id}")
async def delete_chat_session(
    session_id: str,
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Delete a chat session"""
    firebase_uid = current_user.get("uid") or current_user.get("firebase_uid")
    
    result = await db.execute(select(User).where(User.firebase_uid == firebase_uid))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    result = await db.execute(
        select(ChatSession).where(ChatSession.id == session_id, ChatSession.user_id == user.id)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    await db.delete(session)
    await db.commit()
    
    return {"message": "Chat session deleted"}