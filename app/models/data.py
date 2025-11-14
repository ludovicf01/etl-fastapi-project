from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from app.db.base import Base

class CSVData(Base):
    """Modèle générique pour stocker les données CSV"""
    __tablename__ = "file_metadata"
    __table_args__ = {'schema': 'csv_data'}

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    s3_path = Column(String, nullable=False)
    row_count = Column(Integer)
    status = Column(String, default="uploaded")  # uploaded, processing, completed, failed

class OpenDataRecord(Base):
    """Exemple de modèle pour données OpenData spécifiques"""
    __tablename__ = "opendata_records"
    __table_args__ = {'schema': 'csv_data'}

    id = Column(Integer, primary_key=True, index=True)

    # Colonnes génériques - à adapter selon vos données
    code = Column(String, index=True)
    name = Column(String)
    value = Column(Float)
    category = Column(String)
    description = Column(Text)
    date = Column(DateTime)

    # Métadonnées
    source_file = Column(String)
    created_at = Column(DateTime, default=datetime.now())
