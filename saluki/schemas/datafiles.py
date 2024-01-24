import datetime
from typing import Optional
from pydantic import BaseModel, AnyUrl

from ..enums import DataFileType, DataFileStatus


# Shared properties
class DataFileBase(BaseModel):
    slug: str
    description: str
    type: DataFileType
    record_count: Optional[int] = 0
    start_date: datetime.date
    end_date: datetime.date
    status: DataFileStatus


# Extra properties to receive via API on creation
class DataFileCreate(DataFileBase):
    location: Optional[AnyUrl] = None


# Extra properties to receive via API on update
class DataFileUpdate(DataFileBase):
    location: Optional[AnyUrl] = None


# Extra properties stored in DB
class DataFileInDB(DataFileBase):
    id: Optional[int] = None
    location: Optional[AnyUrl] = None


# Additional properties to return via API
class DataFile(DataFileBase):
    download_link: Optional[AnyUrl] = None
