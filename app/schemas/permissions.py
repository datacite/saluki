from ..enums import DataFileType
from pydantic import BaseModel


class DataFilePermission(BaseModel):
    user_id: int
    data_file_id: int


class DataFileTypePermission(BaseModel):
    user_id: int
    data_file_type: DataFileType
