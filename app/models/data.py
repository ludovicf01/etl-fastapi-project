"""Model SQL"""
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel


class CSVData(SQLModel, table=True):
    """CSVData model sql"""
    __tablename__ = "file_metadata"
    __table_args__ = {"schema": "csv_data"}
    id: int | None = Field(default=None, primary_key=True, index=True)
    filename: str = Field(nullable=False)
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    s3_path: str = Field(nullable=False)
    row_count: int = Field(default=None)
    status: str = Field(default="uploaded") # uploaded, processing, completed, failed

class OpenDataRecord(SQLModel, table=True):
    """Exemple de modèle pour données OpenData spécifiques"""
    __tablename__ = "opendata_records"
    __table_args__ = {'schema': 'csv_data'}

    id: int | None = Field(default=None, primary_key=True, index=True)

    # Colonnes génériques - à adapter selon vos données
    code: str = Field(index=True)
    name: str = Field(default=None)
    value: float = Field(default=None)
    category: str = Field(default=None)
    description: str = Field(default=None)
    date: datetime = Field(default=None)

    # Métadonnées
    source_file: str = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
