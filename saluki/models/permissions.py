from sqlalchemy import Column, Enum, ForeignKey, Integer, union_all
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, relationship

from saluki.dependencies.database import Base
from saluki.enums import DataFileType, PermissionType
from saluki.schemas.permissions import DataFilePermission, DataFileTypePermission


class DBDataFilePermission(Base):
    """Allows a user access to an individual data file."""

    __tablename__ = "datafile_permissions"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    data_file_id = Column(Integer, ForeignKey("datafiles.id"), primary_key=True)

    user = relationship(
        "DBUser", back_populates="datafile_permissions"
    )

    datafile = relationship(
        "DBDataFile", back_populates="direct_permissions"
    )

    def __repr__(self):
        return f"<DBDataFilePermission(user_id={self.user_id}, data_file_id={self.data_file_id})>"


class DBDataFileTypePermission(Base):
    """Allows a user access to a specific type of data file."""

    __tablename__ = "datafiletype_permissions"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    data_file_type = Column(Enum(DataFileType), primary_key=True)

    user = relationship(
        "DBUser", back_populates="filetype_permissions"
    )

    datafile = relationship(
        "DBDataFile", back_populates="type_permissions", primaryjoin="foreign(DBDataFileTypePermission.data_file_type) == DBDataFile.type"
    )

    def __repr__(self):
        return f"<DBDataFileTypePermission(user_id={self.user_id}, data_file_type={self.data_file_type})>"


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
