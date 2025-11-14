"""Setting config"""

from typing import List

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Setting app"""
    PROJECT_NAME: str = "ETL FastAPI"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str

    # S3/MinIO
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    S3_ENDPOINT_URL: str
    S3_BUCKET_NAME: str
    S3_REGION: str = "us-east-1"

    # Upload
    MAX_UPLOAD_SIZE: int = 50  # MB
    ALLOWED_EXTENSIONS: List[str] = ["csv", "xlsx"]

    class Config:
        """class config"""
        env_file = ".env"
        case_sensitive = True

settings = Settings()
