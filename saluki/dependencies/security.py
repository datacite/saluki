from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from saluki.dependencies.database import get_database
from saluki.enums import UserLevel
from saluki.models import DBUser, get_user_by_email

from saluki.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)


def get_token_user(token=Depends(oauth2_scheme), action: str = None) -> str | None:
    if token:
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
            email: str = payload.get("sub")
            token_action: str = payload.get("action")
            if email is None or token_action != action:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return email
    else:
        return None


def get_current_user(db=Depends(get_database), token=Depends(oauth2_scheme)) -> DBUser:
    if token:
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
            email: str = payload.get("sub")
            action: str = payload.get("action")
            if email is None or action != "api":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user = get_user_by_email(db=db, email=email)
        if user:
            if user.is_active:
                return user
            else:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
            )
    else:
        return DBUser(name="Anonymous", user_level=UserLevel.anonymous, is_active=True)


class AccessLevelChecker:
    def __init__(self, required_security_level):
        self.required_security_level = required_security_level

    def __call__(self, user=Depends(get_current_user)):
        if not user:
            user_level = UserLevel.anonymous
        else:
            user_level = user.user_level
        if user_level < self.required_security_level:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Insufficient permissions",
            )
        return True


def create_access_token(user: DBUser):
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    data = {"sub": user.email, "action": "api", "exp": expire}
    encoded_jwt = jwt.encode(data, settings.secret_key, algorithm="HS256")
    return encoded_jwt


def create_verification_token(user: DBUser):
    expire = datetime.utcnow() + timedelta(minutes=settings.confirmation_expire_minutes)
    data = {"sub": user.email, "action": "confirm", "exp": expire}
    encoded_jwt = jwt.encode(data, settings.secret_key, algorithm="HS256")
    return encoded_jwt
