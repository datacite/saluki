from fastapi import APIRouter, Depends, HTTPException, status

from saluki.dependencies.database import get_database
from saluki.dependencies.security import AccessLevelChecker, get_current_user
from saluki.enums import UserLevel
from saluki.models.users import (
    create_user,
    get_user_by_email,
    list_user,
    list_users,
    remove_user,
    update_user,
)
from saluki.schemas.users import User, UserCreate, UserInDB, UserUpdate

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        404: {"description": "User not found"},
        403: {"description": "Insufficient permissions"},
    },
)


@user_router.get(
    "/",
    response_model=list[User],
    dependencies=[Depends(AccessLevelChecker(UserLevel.staff))],
)
def get_users(skip: int = 0, limit: int = 100, db=Depends(get_database)):
    return list_users(db=db, skip=skip, limit=limit)


@user_router.get(
    "/{user_id}",
    response_model=User,
    dependencies=[Depends(AccessLevelChecker(UserLevel.user))],
)
def get_user(
    user_id: str, db=Depends(get_database), current_user=Depends(get_current_user)
):
    db_user = list_user(db=db, email=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if current_user == db_user or current_user.user_level >= UserLevel.staff:
        return db_user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
        )


@user_router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def post_user(user: UserCreate, db=Depends(get_database)):
    db_user = create_user(db=db, user_dict=user)
    return db_user


@user_router.put(
    "/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AccessLevelChecker(UserLevel.user))],
)
def put_user(
    user_id: str,
    user: UserUpdate,
    db=Depends(get_database),
    current_user=Depends(get_current_user),
):
    db_user = get_user_by_email(db=db, email=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if current_user == db_user or current_user.user_level >= UserLevel.staff:
        # Don't let a level be increased higher than the level below the current user
        if user.user_level and user.user_level >= current_user.user_level:
            user.user_level = None
        db_user = update_user(db=db, user=db_user, user_dict=user)
        return db_user
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
        )


@user_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AccessLevelChecker(UserLevel.staff))],
)
def delete_user(user_id: str, db=Depends(get_database)):
    db_user = get_user_by_email(db=db, email=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return remove_user(db=db, user=db_user)
