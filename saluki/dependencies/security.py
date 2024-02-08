from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from saluki.dependencies.database import get_database
from saluki.enums import UserLevel
from saluki.models import DBUser, get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

# TODO: Replace these with ENV variables
SECRET_KEY = "11e3fe012c296e83632b50b920532ca42901d295043cbefcb662ac55ec5d587a"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440


def get_current_user(db=Depends(get_database), token=Depends(oauth2_scheme)) -> DBUser:
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"},
                )
        except JWTError:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"},
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
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub": user.email, "exp": expire}
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
