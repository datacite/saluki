from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from routers.datafiles import datafile_router
from routers.permissions import permissions_router
from routers.users import user_router
from saluki.dependencies.database import get_database
from saluki.models import get_user_by_email


app = FastAPI()

app.include_router(user_router)
app.include_router(datafile_router)
app.include_router(permissions_router)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db=Depends(get_database)):
    user = get_user_by_email(db=db, email=form_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    if not user.verify_password(form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    return {"access_token": user.email, "token_type": "bearer"}