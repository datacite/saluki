from ..enums import DataFileType, DataFileStatus
from ..dependencies.database import Base
from sqlalchemy import Column, Integer, String, Text, Date, Enum


class DBDataFile(Base):
    """Represents a data file."""
    __tablename__ = "datafiles"

    id = Column(Integer, primary_key=True)
    slug = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    type = Column(Enum(DataFileType), nullable=False, index=True)
    record_count = Column(Integer, nullable=False, default=0)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(Enum(DataFileStatus), nullable=False, index=True)
    location = Column(String, nullable=True)

    @property
    def download_link(self):
        """Generate a download link for the data file."""
        return self.location  # Temporary - replace with AWS SDK call later on
