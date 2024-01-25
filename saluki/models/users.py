from passlib.context import CryptContext
from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, relationship

from saluki.dependencies.database import Base
from saluki.enums import UserLevel
from saluki.schemas.users import UserCreate, UserUpdate

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

    datafile_permissions = relationship(
        "DBDataFilePermission", back_populates="user", cascade="all, delete-orphan"
    )
    filetype_permissions = relationship(
        "DBDataFileTypePermission", back_populates="user", cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password = password_context.hash(password)

    def verify_password(self, password):
        return password_context.verify(password, self.password)


def list_users(*, db: Session, skip: int = 0, limit: int = 100) -> list[DBUser]:
    return db.query(DBUser).offset(skip).limit(limit).all()


def list_user(*, db: Session, email: str) -> DBUser | None:
    return get_user_by_email(db=db, email=email)


def create_user(*, db: Session, user_dict: UserCreate) -> DBUser:
    user = DBUser(**user_dict.model_dump())
    user.set_password(user_dict.password)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(*, db: Session, user: DBUser, user_dict: UserUpdate) -> DBUser:
    user.name = user_dict.name
    user.email = user_dict.email
    if user_dict.password:
        user.set_password(user_dict.password)

    db.commit()
    db.refresh(user)
    return user


def remove_user(*, db: Session, user: DBUser) -> bool:
    try:
        db.delete(user)
        db.commit()
        return True
    except SQLAlchemyError as e:
        return False


def get_user_by_email(*, db: Session, email: str) -> DBUser | None:
    return db.query(DBUser).filter(DBUser.email == email).first()


def authenticate_user(*, db: Session, email: str, password: str) -> DBUser | None:
    user = get_user_by_email(db=db, email=email)
    if not user:
        return None
    if not user.verify_password(password):
        return None
    return user
