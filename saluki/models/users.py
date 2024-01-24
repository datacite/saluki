from saluki.dependencies.database import Base
from saluki.enums import UserLevel
from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from saluki.schemas.users import UserCreate

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class DBUser(Base):
    """Represents a user."""

    __tablename__ = "users"

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


def create_user(*, db: Session, user_dict: UserCreate) -> DBUser:
    user = DBUser(**user_dict.model_dump())
    user.set_password(user_dict.password)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(*, db: Session, user: DBUser, user_dict: UserCreate) -> DBUser:
    user.name = user_dict.name
    user.email = user_dict.email
    user.set_password(user_dict.password)

    db.commit()
    db.refresh(user)
    return user


def remove_user(*, db: Session, user: DBUser) -> bool:
    db.delete(user)
    db.commit()
    return True


def get_user_by_email(*, db: Session, email: str) -> DBUser | None:
    return db.query(DBUser).filter(DBUser.email == email).first()


def authenticate_user(*, db: Session, email: str, password: str) -> DBUser | None:
    user = get_user_by_email(db=db, email=email)
    if not user:
        return None
    if not user.verify_password(password):
        return None
    return user

