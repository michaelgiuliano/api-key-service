from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    """User model for authentication and API key ownership.
    
    Attributes:
        id: Primary key
        email: Unique email address
        hashed_password: Bcrypt hashed password
        api_keys: Relationship to user's API keys
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str]

    api_keys: Mapped[list["ApiKey"]] = relationship("ApiKey", back_populates="user", cascade="all, delete-orphan")