from fastapi import APIRouter, Depends, HTTPException, status

from saluki.models.users import DBUser, create_user, get_user_by_email, update_user, remove_user
from saluki.schemas.users import UserCreate, User, UserInDB
from saluki.dependencies.database import get_database


user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "User not found"}, 403: {"description": "Insufficient permissions"}},
)


@user_router.get("/", response_model=list[User])
def get_users(skip: int = 0, limit: int = 100, db=Depends(get_database)):
    users = db.query(DBUser).offset(skip).limit(limit).all()
    return users


@user_router.get("/{user_id}", response_model=UserInDB)
def get_user(user_id: str, db=Depends(get_database)):
    db_user = get_user_by_email(db=db, email=user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@user_router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def post_user(user: UserCreate, db=Depends(get_database)):
    db_user = create_user(db=db, user_dict=user)
    return db_user


@user_router.put("/{user_id}", response_model=User)
def put_user(user_id: str, user: UserCreate, db=Depends(get_database)):
    db_user = get_user_by_email(db=db, email=user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db_user = update_user(db=db, user=db_user, user_dict=user)
    return db_user


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db=Depends(get_database)):
    db_user = get_user_by_email(db=db, email=user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return remove_user(db=db, user=db_user)

