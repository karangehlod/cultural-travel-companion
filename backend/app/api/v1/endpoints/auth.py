"""
Auth endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.core.security import get_current_user_firebase, create_access_token, create_refresh_token
from app.core.firebase import verify_firebase_token
from app.models.user import User
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter()


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    firebase_uid: str
    email: str
    display_name: Optional[str]
    photo_url: Optional[str]
    role: str
    created_at: str
    
    class Config:
        from_attributes = True


@router.post("/verify-token", response_model=TokenResponse)
async def verify_token(
    id_token: str,
    db: AsyncSession = Depends(get_db),
):
    """Verify Firebase ID token and create session"""
    try:
        decoded = await verify_firebase_token(id_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    firebase_uid = decoded.get("uid")
    email = decoded.get("email")
    display_name = decoded.get("name")
    photo_url = decoded.get("picture")
    
    # Get or create user
    result = await db.execute(select(User).where(User.firebase_uid == firebase_uid))
    user = result.scalar_one_or_none()
    
    if not user:
        user = User(
            firebase_uid=firebase_uid,
            email=email,
            display_name=display_name,
            photo_url=photo_url,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
    else:
        # Update user info
        user.display_name = display_name or user.display_name
        user.photo_url = photo_url or user.photo_url
        user.last_login_at = datetime.utcnow()
        await db.commit()
    
    # Create tokens
    access_token = create_access_token(data={"sub": user.id, "firebase_uid": firebase_uid})
    refresh_token = create_refresh_token(data={"sub": user.id, "firebase_uid": firebase_uid})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db),
):
    """Refresh access token"""
    from app.core.security import decode_token
    
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        
        user_id = payload.get("sub")
        firebase_uid = payload.get("firebase_uid")
        
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        access_token = create_access_token(data={"sub": user.id, "firebase_uid": firebase_uid})
        new_refresh_token = create_refresh_token(data={"sub": user.id, "firebase_uid": firebase_uid})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=new_refresh_token,
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: dict = Depends(get_current_user_firebase),
    db: AsyncSession = Depends(get_db),
):
    """Get current user profile"""
    firebase_uid = current_user.get("uid") or current_user.get("firebase_uid")
    
    result = await db.execute(select(User).where(User.firebase_uid == firebase_uid))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=user.id,
        firebase_uid=user.firebase_uid,
        email=user.email,
        display_name=user.display_name,
        photo_url=user.photo_url,
        role=user.role.value,
        created_at=user.created_at.isoformat(),
    )