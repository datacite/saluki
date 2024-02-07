from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from saluki.dependencies.database import get_database
from saluki.enums import UserLevel
from saluki.models import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(db=Depends(get_database), token=Depends(oauth2_scheme)):
    user = get_user_by_email(db=db, email=token)
    if user and not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return user


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

