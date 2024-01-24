from ..enums import DataFileType
from ..dependencies.database import Base
from sqlalchemy import Column, Integer, Enum, ForeignKey


class DBDataFilePermission(Base):
    """Allows a user access to an individual data file."""
    __tablename__ = "datafile_permissions"

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    data_file_id = Column(Integer, ForeignKey('datafiles.id'), primary_key=True)


class DBDataFileTypePermission(Base):
    """Allows a user access to a specific type of data file."""
    __tablename__ = "datafiletype_permissions"

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    data_file_type = Column(Enum(DataFileType), primary_key=True)
