from fastapi import APIRouter, Depends, HTTPException, status

from saluki.dependencies.database import get_database
from saluki.enums import PermissionType
from saluki.models.datafiles import list_datafile
from saluki.models.users import list_user
from saluki.models.permissions import (
    create_permission,
    get_permission_by_id_and_type,
    remove_permission,
)
from saluki.schemas.permissions import DataFilePermission, DataFileTypePermission

permissions_router = APIRouter(
    prefix="/permissions",
    tags=["permissions"],
    responses={
        404: {"description": "Permission not found"},
        403: {"description": "Insufficient permissions"},
    },
)


@permissions_router.get(
    "/datafile/{data_file_id}",
    response_model=list[DataFilePermission | DataFileTypePermission],
)
def get_permissions_for_datafile(data_file_id: str, db=Depends(get_database)):
    datafile = list_datafile(db=db, slug=data_file_id)
    if not datafile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Data file not found"
        )
    return datafile.permissions


@permissions_router.get(
    "/user/{user_id}", response_model=list[DataFilePermission | DataFileTypePermission]
)
def get_permissions_for_user(user_id: str, db=Depends(get_database)):
    user = list_user(db=db, email=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user.permissions


@permissions_router.post(
    "/",
    response_model=DataFilePermission | DataFileTypePermission,
    status_code=status.HTTP_201_CREATED,
)
def post_permission(
    permission: DataFilePermission | DataFileTypePermission, db=Depends(get_database)
):
    return create_permission(db=db, permission_dict=permission)


@permissions_router.delete(
    "/{permission_type}/{permission_id}", status_code=status.HTTP_204_NO_CONTENT
)
def delete_permission(
    permission_type: PermissionType, permission_id: int, db=Depends(get_database)
):
    permission = get_permission_by_id_and_type(
        db=db, permission_id=permission_id, permission_type=permission_type
    )
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found"
        )
    return remove_permission(db=db, permission=permission)
