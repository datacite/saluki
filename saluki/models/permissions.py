from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from . import DBDataFile
from ..enums import DataFileType, PermissionType
from ..dependencies.database import Base
from sqlalchemy import Column, Integer, Enum, ForeignKey

from ..schemas.permissions import DataFileTypePermission, DataFilePermission


class DBDataFilePermission(Base):
    """Allows a user access to an individual data file."""

    __tablename__ = "datafile_permissions"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    data_file_id = Column(Integer, ForeignKey("datafiles.id"), primary_key=True)


class DBDataFileTypePermission(Base):
    """Allows a user access to a specific type of data file."""

    __tablename__ = "datafiletype_permissions"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    data_file_type = Column(Enum(DataFileType), primary_key=True)


def get_permission_by_id_and_type(
    *, db: Session, permission_id: int, permission_type: PermissionType
) -> DBDataFileTypePermission | DBDataFilePermission:
    if permission_type == PermissionType.filetype:
        return (
            db.query(DBDataFileTypePermission)
            .filter(DBDataFileTypePermission.id == permission_id)
            .first()
        )
    else:
        return (
            db.query(DBDataFilePermission)
            .filter(DBDataFilePermission.id == permission_id)
            .first()
        )


def list_permissions_for_user(
    *, db: Session, user_id: int, skip: int = 0, limit: int = 100
) -> list[DBDataFileTypePermission | DBDataFilePermission]:
    return (
        db.query(DBDataFileTypePermission, DBDataFilePermission)
        .filter(
            DBDataFileTypePermission.user_id == user_id,
            DBDataFilePermission.user_id == user_id,
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def list_permissions_for_datafile(
    *, db: Session, datafile_id: int, skip: int = 0, limit: int = 100
) -> list[DBDataFileTypePermission | DBDataFilePermission]:
    return (
        db.query(DBDataFileTypePermission, DBDataFilePermission)
        .join(DBDataFile)
        .filter(
            DBDataFileTypePermission.data_file_type == DBDataFile.type,
            DBDataFilePermission.data_file_id == datafile_id,
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_permission(
    *, db: Session, permission_dict: DataFileTypePermission | DataFilePermission
) -> DBDataFileTypePermission | DBDataFilePermission:
    if isinstance(permission_dict, DataFileTypePermission):
        permission = DBDataFileTypePermission(**permission_dict.model_dump())
    else:
        permission = DBDataFilePermission(**permission_dict.model_dump())
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission


def remove_permission(
    *, db: Session, permission: DataFileTypePermission | DataFilePermission
) -> bool:
    try:
        db.delete(permission)
        db.commit()
        return True
    except SQLAlchemyError as e:
        return False
