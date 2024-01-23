from ..enums import DataFileType
from ..dependencies.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Text, Date, Enum


class DataFile(Base):
    """Represents a data file."""
    id = Column(Integer, primary_key=True)
    slug = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    type = Column(Enum(DataFileType), nullable=False, index=True)
    record_count = Column(Integer, nullable=False, default=0)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String, nullable=False, index=True)
    location = Column(String, nullable=True)
    is_public = Column(Boolean, default=False, index=True)


