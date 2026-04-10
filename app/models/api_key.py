from sqlalchemy import String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from app.db.base import Base


class ApiKey(Base):
    """API key model for secure authentication.
    
    Attributes:
    
        id: Primary key
        user_id: Foreign key to user

        prefix: Public prefix for identification
        identifier: Unique identifier

        hashed_key: Bcrypt hashed full key

        name: User-defined name
        created_at: Creation timestamp
        last_used_at: Last usage timestamp
        expires_at: Expiration timestamp

        is_active: Active status
        revoked_at: Revocation timestamp

        user: Relationship to owner
    
    """
    __tablename__ = "api_keys"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)

    prefix: Mapped[str] = mapped_column(String(8), index=True)
    identifier: Mapped[str] = mapped_column(String(32), unique=True, index=True)

    hashed_key: Mapped[str] = mapped_column(String(255))

    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_used_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    revoked_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="api_keys")
