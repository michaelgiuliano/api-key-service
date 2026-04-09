from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.auth_service import create_user, login_user
from app.api.deps import get_current_user
from app.core.security import bearer_scheme


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
def signup(email: str, password: str, db: Session = Depends(get_db)):
    user = create_user(db, email, password)
    return {"id": user.id, "email": user.email}


@router.post("/login")
def login(email: str, password: str, db: Session = Depends(get_db)):
    token = login_user(db, email, password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token}


@router.get("/me")
def get_me(
    current_user = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)
):
    return {
        "id": current_user.id,
        "email": current_user.email
    }