"""ETL Model"""
from datetime import datetime
from pydantic import BaseModel


class FileUploadResponse(BaseModel):
    """response"""
    filename: str
    size: int
    s3_path: str
    upload_time: datetime
    status: str = "uploaded"
