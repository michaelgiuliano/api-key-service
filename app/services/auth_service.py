from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token


def create_user(db: Session, email: str, password: str) -> Optional[User]:
    """Create a new user with hashed password.
    
    Args:
        db: Database session
        email: User email address
        password: Plain text password
        
    Returns:
        User object if successful, None if email already exists
    """
    user = User(
        email=email,
        hashed_password=hash_password(password)
    )
    db.add(user)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return None
    
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user with email and password.
    
    Args:
        db: Database session
        email: User email address
        password: Plain text password
        
    Returns:
        User object if credentials valid, None otherwise
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def login_user(db: Session, email: str, password: str) -> Optional[str]:
    """Authenticate user and generate JWT token.
    
    Args:
        db: Database session
        email: User email address
        password: Plain text password
        
    Returns:
        JWT token string if successful, None otherwise
    """
    user = authenticate_user(db, email, password)
    if not user:
        return None
    token = create_access_token({"sub": str(user.id)})
    return token
