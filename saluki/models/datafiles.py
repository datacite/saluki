from fastapi.encoders import jsonable_encoder
from sqlalchemy import Column, Date, Enum, Integer, String, Text
from sqlalchemy.orm import Session

from saluki.dependencies.database import Base
from saluki.enums import DataFileStatus, DataFileType
from saluki.schemas.datafiles import DataFileCreate, DataFileUpdate


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
    doi = Column(String, nullable=True)

    @property
    def download_link(self):
        """Generate a download link for the data file."""
        return self.location  # Temporary - replace with AWS SDK call later on

    def __repr__(self):
        return f"<DBDataFile(id={self.id}, slug={self.slug}, type={self.type}, status={self.status})>"


def list_datafiles(*, db: Session, skip: int = 0, limit: int = 100) -> list[DBDataFile]:
    return db.query(DBDataFile).offset(skip).limit(limit).all()


def list_datafile(*, db: Session, slug: str) -> DBDataFile:
    return db.query(DBDataFile).filter(DBDataFile.slug == slug).first()


def create_datafile(*, db: Session, datafile_dict: DataFileCreate) -> DBDataFile:
    datafile = DBDataFile(**datafile_dict.model_dump())
    # Force the location to be a string rather than Pydantic's AnyURL type
    datafile.location = str(datafile.location)
    db.add(datafile)
    db.commit()
    db.refresh(datafile)
    return datafile


def update_datafile(
    *, db: Session, datafile: DBDataFile, datafile_dict: DataFileUpdate
) -> DBDataFile:
    datafile.description = datafile_dict.description
    datafile.type = datafile_dict.type
    datafile.record_count = datafile_dict.record_count
    datafile.start_date = datafile_dict.start_date
    datafile.end_date = datafile_dict.end_date
    datafile.status = datafile_dict.status
    datafile.location = str(datafile_dict.location)
    datafile.doi = datafile_dict.doi

    db.commit()
    db.refresh(datafile)
    return datafile


def remove_datafile(*, db: Session, datafile: DBDataFile) -> bool:
    datafile.status = DataFileStatus.deleted
    db.commit()
    return True
