from fastapi import APIRouter, Depends, HTTPException, status

from saluki.dependencies.database import get_database
from saluki.dependencies.security import AccessLevelChecker, get_current_user
from saluki.enums import UserLevel
from saluki.models.datafiles import (
    create_datafile,
    list_datafile,
    list_datafiles,
    remove_datafile,
    update_datafile,
)
from saluki.schemas.datafiles import (
    DataFile,
    DataFileCreate,
    DataFileInDB,
    DataFileUpdate,
)

datafile_router = APIRouter(
    prefix="/datafiles",
    tags=["datafiles"],
    responses={
        404: {"description": "Data File not found"},
        403: {"description": "Insufficient permissions"},
    },
)


@datafile_router.get("/", response_model=list[DataFile])
def get_datafiles(
    skip: int = 0,
    limit: int = 100,
    db=Depends(get_database),
    current_user=Depends(get_current_user),
):
    if current_user.user_level >= UserLevel.editor:
        return list_datafiles(db=db, skip=skip, limit=limit)
    elif current_user.user_level == UserLevel.anonymous:
        # Need to think about this - three possible options:
        # 1. Bring back the is_public attribute on the DataFile model
        # 2. Add an Anonymous user to the DB, so it can be granted permissions using the normal flow
        # 3. Define in code the types of data files that can be accessed by an Anonymous user and use a different DB query
        return []
    else:
        return current_user.datafiles


@datafile_router.get("/{datafile_id}", response_model=DataFile)
def get_datafile(
    datafile_id: str, db=Depends(get_database), current_user=Depends(get_current_user)
):
    db_datafile = list_datafile(db=db, slug=datafile_id)
    if not db_datafile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Data File not found"
        )
    if (
        current_user.user_level >= UserLevel.editor
        or db_datafile in current_user.datafiles
    ):
        return db_datafile
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions"
        )


@datafile_router.post(
    "/",
    response_model=DataFile,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(AccessLevelChecker(UserLevel.editor))],
)
def post_datafile(datafile: DataFileCreate, db=Depends(get_database)):
    db_datafile = create_datafile(db=db, datafile_dict=datafile)
    return db_datafile


@datafile_router.put(
    "/{datafile_id}",
    response_model=DataFile,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(AccessLevelChecker(UserLevel.editor))],
)
def put_datafile(datafile_id: str, datafile: DataFileUpdate, db=Depends(get_database)):
    db_datafile = get_datafile(db=db, slug=datafile_id)
    if not db_datafile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Data File not found"
        )
    db_datafile = update_datafile(db=db, datafile=db_datafile, datafile_dict=datafile)
    return db_datafile


@datafile_router.delete(
    "/{datafile_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(AccessLevelChecker(UserLevel.editor))],
)
def delete_datafile(datafile_id: str, db=Depends(get_database)):
    db_datafile = get_datafile(db=db, slug=datafile_id)
    if not db_datafile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Data File not found"
        )
    return remove_datafile(db=db, datafile=db_datafile)
