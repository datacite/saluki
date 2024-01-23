from ..enums import DataFileType
from ..dependencies.database import Base
from sqlalchemy import Column, Integer, Enum, ForeignKey


class DataFilePermission(Base):
    """Allows a user access to an individual data file."""
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    data_file_id = Column(Integer, ForeignKey('datafile.id'), primary_key=True)


class DataFileTypePermission(Base):
    """Allows a user access to a specific type of data file."""
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    data_file_type = Column(Enum(DataFileType), primary_key=True)
