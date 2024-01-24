from pydantic import BaseModel

from ..enums import DataFileType


class DataFilePermission(BaseModel):
    user_id: int
    data_file_id: int


class DataFileTypePermission(BaseModel):
    user_id: int
    data_file_type: DataFileType
