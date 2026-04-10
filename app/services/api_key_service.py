from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from app.models.api_key import ApiKey
from app.core.security import (
    generate_api_key_prefix,
    generate_api_key_identifier,
    generate_api_key_secret,
    generate_full_api_key,
    hash_api_key,
    verify_api_key
)


def create_api_key(db: Session, user_id: int, name: str) -> tuple[ApiKey, str]:
    """
    Create a new API key for a user.

    Returns:
        tuple: (ApiKey object, full_api_key_string)
        The full API key is only returned once during creation.
    """

    prefix = generate_api_key_prefix()
    identifier = generate_api_key_identifier()
    secret = generate_api_key_secret()
    full_key = generate_full_api_key(prefix, secret)

    hashed_key = hash_api_key(full_key)

    api_key = ApiKey(
        user_id=user_id,
        prefix=prefix,
        identifier=identifier,
        hashed_key=hashed_key,
        name=name,
        created_at=datetime.utcnow()
    )
    
    db.add(api_key)
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Failed to create API key - identifier collision")
    
    db.refresh(api_key)
    return api_key, full_key


def get_user_api_keys(db: Session, user_id: int) -> list[ApiKey]:
    """Get all API keys for a user (with masked keys)."""
    return db.query(ApiKey).filter(ApiKey.user_id == user_id).all()


def get_api_key_by_identifier(db: Session, identifier: str) -> ApiKey | None:
    """Get API key by identifier (for validation)."""
    return db.query(ApiKey).filter(ApiKey.identifier == identifier).first()


def verify_api_key_by_identifier(db: Session, identifier: str, provided_key: str) -> ApiKey | None:
    """Verify an API key and return the ApiKey object if valid."""
    api_key = get_api_key_by_identifier(db, identifier)
    
    if not api_key:
        return None
    
    if not api_key.is_active:
        return None
    
    if api_key.revoked_at:
        return None
    
    if not verify_api_key(provided_key, api_key.hashed_key):
        return None
    
    api_key.last_used_at = datetime.utcnow()
    db.commit()
    
    return api_key


def revoke_api_key(db: Session, user_id: int, api_key_id: int) -> bool:
    """Revoke an API key."""
    api_key = db.query(ApiKey).filter(
        ApiKey.id == api_key_id,
        ApiKey.user_id == user_id
    ).first()
    
    if not api_key:
        return False
    
    api_key.is_active = False
    api_key.revoked_at = datetime.utcnow()
    
    db.commit()
    return True


def delete_api_key(db: Session, user_id: int, api_key_id: int) -> bool:
    """Permanently delete an API key."""
    api_key = db.query(ApiKey).filter(
        ApiKey.id == api_key_id,
        ApiKey.user_id == user_id
    ).first()
    
    if not api_key:
        return False
    
    db.delete(api_key)
    db.commit()
    return True
