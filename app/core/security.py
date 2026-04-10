import jwt
import secrets
import string
from passlib.context import CryptContext
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer

from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

bearer_scheme = HTTPBearer()


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_access_token(data: dict) -> str:
    if not data or "sub" not in data:
        raise ValueError("Token data must contain 'sub' field")
    
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    
    try:
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    except Exception as e:
        raise ValueError(f"Failed to create access token: {str(e)}")


def generate_api_key_prefix() -> str:
    """Generate a random 8-character prefix for API key identification."""
    return secrets.token_hex(4).upper()


def generate_api_key_identifier() -> str:
    """Generate a unique 32-character identifier for API key."""
    return secrets.token_urlsafe(24)


def generate_api_key_secret(length: int = 32) -> str:
    """Generate a cryptographically secure API key secret."""
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def generate_full_api_key(prefix: str, secret: str) -> str:
    """Combine prefix and secret into full API key format."""
    return f"{prefix}_{secret}"


def hash_api_key(api_key: str) -> str:
    """Hash an API key for secure storage."""
    return pwd_context.hash(api_key)


def verify_api_key(api_key: str, hashed_key: str) -> bool:
    """Verify an API key against its hash."""
    return pwd_context.verify(api_key, hashed_key)