from fastapi.security import OAuth2PasswordBearer
from saluki.models import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(db, token):
    user = get_user_by_email(db=db, email=token)
    return user
