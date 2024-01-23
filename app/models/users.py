from ..dependencies.database import Base
from ..enums import UserLevel
from sqlalchemy import Column, Integer, String, Boolean, Enum


class User(Base):
    """Represents a user."""
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=True)
    password = Column(String, nullable=False)
    user_level = Column(Enum(UserLevel), nullable=False, default=0)
    is_active = Column(Boolean, default=False)
