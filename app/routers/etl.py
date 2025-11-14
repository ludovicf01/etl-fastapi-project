import logging
from pathlib import Path
from app.db.session import get_db
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.services import etl_service
from app.models.data import CSVData

router = APIRouter()
logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("./data")

def process_file_background(filename: str, db: Session):
    """Fonction pour traiter le fichier en arrière-plan"""
    try:
        file_path = UPLOAD_DIR / filename
        s3_path = f"s3://csv-files/uploads/{filename}"
        etl_service.ETLService.process_csv_file(db, str(file_path), filename, s3_path)
    except Exception as e:
        logger.error(f"Background processing error: {e}")

@router.post("/process/{filename}", response_model=dict)
async def process_csv(
    filename: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
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
    existing = db.query(CSVData).filter(CSVData.filename == filename).first()
    if existing and existing.status == "completed":
        raise HTTPException(status_code=400, detail="File already processed")

    # Lancer le traitement en arrière-plan
    background_tasks.add_task(process_file_background, filename, db)

    return {
        "message": "ETL process started",
        "filename": filename,
        "status": "processing"
    }
