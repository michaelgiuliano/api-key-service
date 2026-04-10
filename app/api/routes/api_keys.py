from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.services.api_key_service import create_api_key, get_user_api_keys, revoke_api_key

router = APIRouter(prefix="/api-keys", tags=["api-keys"])


class CreateApiKeyRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Name for the API key")


class ApiKeyResponse(BaseModel):
    id: int
    prefix: str
    identifier: str
    name: str
    created_at: str
    last_used_at: str | None
    expires_at: str | None
    is_active: bool


class CreateApiKeyResponse(BaseModel):
    api_key: ApiKeyResponse
    full_key: str = Field(description="The complete API key - only returned once")


@router.post("/", response_model=CreateApiKeyResponse)
def create_api_key_endpoint(
    request: CreateApiKeyRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new API key. The full key is only returned once."""
    try:
        api_key, full_key = create_api_key(db, current_user.id, request.name)
        
        return CreateApiKeyResponse(
            api_key=ApiKeyResponse(
                id=api_key.id,
                prefix=api_key.prefix,
                identifier=api_key.identifier,
                name=api_key.name,
                created_at=api_key.created_at.isoformat(),
                last_used_at=api_key.last_used_at.isoformat() if api_key.last_used_at else None,
                expires_at=api_key.expires_at.isoformat() if api_key.expires_at else None,
                is_active=api_key.is_active
            ),
            full_key=full_key
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to create API key")


@router.get("/", response_model=list[ApiKeyResponse])
def list_api_keys(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all API keys for the current user (keys are masked for security)."""
    try:
        api_keys = get_user_api_keys(db, current_user.id)
        
        return [
            ApiKeyResponse(
                id=api_key.id,
                prefix=api_key.prefix,
                identifier=api_key.identifier,
                name=api_key.name,
                created_at=api_key.created_at.isoformat(),
                last_used_at=api_key.last_used_at.isoformat() if api_key.last_used_at else None,
                expires_at=api_key.expires_at.isoformat() if api_key.expires_at else None,
                is_active=api_key.is_active
            )
            for api_key in api_keys
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to retrieve API keys")


@router.delete("/{api_key_id}")
def revoke_api_key_endpoint(
    api_key_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Revoke an API key (soft delete - sets is_active=False and revoked_at)."""
    try:
        success = revoke_api_key(db, current_user.id, api_key_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="API key not found")
        
        return {"message": "API key revoked successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to revoke API key")
