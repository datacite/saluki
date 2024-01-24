from fastapi import FastAPI
from routers.users import user_router
from routers.datafiles import datafile_router
from routers.permissions import permissions_router

app = FastAPI()

app.include_router(user_router)
app.include_router(datafile_router)
app.include_router(permissions_router)


@app.get("/")
def root():
    return {"message": "Hello World"}
