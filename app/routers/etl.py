"""ETL service"""
from pathlib import Path
import logging
from fastapi import APIRouter, HTTPException, BackgroundTasks
from sqlmodel import select
from sqlalchemy.exc import SQLAlchemyError
from app.db.session import SessionDep
from app.models.data import CSVData
from app.services import etl_service

router = APIRouter()
logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("./data")

def process_file_background(filename: str, db:SessionDep):
    """Fonction pour traiter le fichier en arrière-plan"""
    try:
        file_path = UPLOAD_DIR / filename
        s3_path = f"s3://csv-files/uploads/{filename}"
        result = etl_service.ETLService.process_csv_file(db, str(file_path), filename, s3_path)
        print(result)
    except SQLAlchemyError as e:
        logger.error("Background processing error: %s", e)

@router.post("/process/{filename}", response_model=dict)
async def process_csv(
    filename: str,
    background_tasks: BackgroundTasks,
    db_bis: SessionDep
):
    """
    Lancer le traitement ETL d'un fichier CSV
    - Lecture
    - Nettoyage
    - Insertion en base
    """
    file_path = UPLOAD_DIR / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    # Vérifier si déjà traité
    existing = db_bis.exec(select(CSVData).where(CSVData.filename == filename)).first()
    if existing and existing.status == "completed":
        raise HTTPException(status_code=400, detail="File already processed")

    # Lancer le traitement en arrière-plan
    background_tasks.add_task(process_file_background, filename, db_bis)

    return {
        "message": "ETL process started",
        "filename": filename,
        "status": "processing"
    }
