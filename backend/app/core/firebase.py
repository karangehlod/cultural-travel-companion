"""
Firebase configuration and initialization
"""
import firebase_admin
from firebase_admin import credentials, firestore, auth
from typing import Optional

from app.core.config import settings


_firebase_app: firebase_admin.App | None = None
_firestore_client: firestore.AsyncClient | None = None


def init_firebase() -> None:
    """Initialize Firebase Admin SDK"""
    global _firebase_app
    
    if _firebase_app is not None:
        return
    
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": settings.FIREBASE_PROJECT_ID,
        "private_key_id": settings.FIREBASE_PRIVATE_KEY_ID,
        "private_key": settings.FIREBASE_PRIVATE_KEY.replace("\\n", "\n"),
        "client_email": settings.FIREBASE_CLIENT_EMAIL,
        "client_id": settings.FIREBASE_CLIENT_ID,
        "auth_uri": settings.FIREBASE_AUTH_URI,
        "token_uri": settings.FIREBASE_TOKEN_URI,
    })
    
    _firebase_app = firebase_admin.initialize_app(cred)


def get_firebase_app() -> firebase_admin.App:
    """Get Firebase app instance"""
    if _firebase_app is None:
        init_firebase()
    return _firebase_app


async def get_firestore() -> firestore.AsyncClient:
    """Get Firestore async client"""
    global _firestore_client
    
    if _firestore_client is None:
        get_firebase_app()
        _firestore_client = firestore.AsyncClient()
    
    return _firestore_client


async def get_firebase_auth():
    """Get Firebase Auth instance"""
    get_firebase_app()
    return auth


async def verify_firebase_token(id_token: str) -> dict:
    """Verify Firebase ID token"""
    auth_client = await get_firebase_auth()
    try:
        decoded_token = auth_client.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        raise ValueError(f"Invalid token: {str(e)}")


async def get_user_by_uid(uid: str) -> auth.UserRecord | None:
    """Get user by UID"""
    auth_client = await get_firebase_auth()
    try:
        return auth_client.get_user(uid)
    except auth.UserNotFoundError:
        return None