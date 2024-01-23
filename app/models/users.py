from ..dependencies.database import Base
from ..enums import UserLevel
from sqlalchemy import Column, Integer, String, Boolean, Enum
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    """Represents a user."""
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True, index=True)
    name = Column(String, nullable=True)
    password = Column(String, nullable=False)
    user_level = Column(Enum(UserLevel), nullable=False, default=0)
    is_active = Column(Boolean, default=False)

    def set_password(self, password):
        self.password = password_context.hash(password)

    def verify_password(self, password):
        return password_context.verify(password, self.password)

