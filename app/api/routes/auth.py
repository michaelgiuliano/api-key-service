from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services.auth_service import create_user, login_user


router = APIRouter(prefix="/auth", tags=["auth"])


class SignupRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup", response_model=Dict[str, Any])
def signup(data: SignupRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Register a new user account.
    
    Args:
        data: Signup request with email and password
        db: Database session
        
    Returns:
        User ID and email
        
    Raises:
        HTTPException: If email already registered or server error
    """
    try:
        user = create_user(db, data.email, data.password)

        if not user:
            raise HTTPException(status_code=409, detail="Email already registered")

        return {"id": user.id, "email": user.email}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create user")


@router.post("/login", response_model=Dict[str, Any])
def login(data: LoginRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Authenticate user and return JWT token.
    
    Args:
        data: Login request with email and password
        db: Database session
        
    Returns:
        JWT access token and token type
        
    Raises:
        HTTPException: If credentials invalid or server error
    """
    try:
        token = login_user(db, data.email, data.password)

        if not token:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        return {
            "access_token": token,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to authenticate user")


@router.get("/me", response_model=Dict[str, Any])
def get_me(current_user: User = Depends(get_current_user)) -> Dict[str, Any]:
    """Get current user profile.
    
    Args:
        current_user: Authenticated user from JWT token
        
    Returns:
        User ID and email
        
    Raises:
        HTTPException: If server error occurs
    """
    try:
        return {
            "id": current_user.id,
            "email": current_user.email
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve user profile")
