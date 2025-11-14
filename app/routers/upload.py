"""upload"""
import logging
from datetime import datetime
from pathlib import Path
import aiofiles
from fastapi import APIRouter, File, HTTPException, UploadFile


from app.services.s3_service import s3_service
from app.config import settings

from app.schemas.etl import FileUploadResponse


router = APIRouter()
logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("./data")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload/")
async def upload_csv_file(file: UploadFile = File(...)):
    """
    Upload un fichier CSV
    - Sauvegarde locale temporaire
    - Upload vers S3/MinIO
    - Retourne les métadonnées
    """
    # Validation de l'extension
    file_ext = file.filename.split('.')[-1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File extension not allowed. Allowed: {settings.ALLOWED_EXTENSIONS}"
        )

    # Validation de la taille (optionnel, FastAPI gère déjà)
    file_size = 0

    try:
        # Sauvegarder temporairement
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = UPLOAD_DIR / safe_filename

        async with aiofiles.open(file_path, 'wb') as out_file:
            while content := await file.read(1024 * 1024):  # 1MB chunks
                file_size += len(content)
                await out_file.write(content)

        # Vérifier la taille
        if file_size > settings.MAX_UPLOAD_SIZE * 1024 * 1024:
            file_path.unlink()  # Supprimer le fichier
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max: {settings.MAX_UPLOAD_SIZE}MB"
            )

        # Upload vers S3
        s3_key = f"uploads/{safe_filename}"
        s3_path = s3_service.upload_file(str(file_path), s3_key)

        logger.info(f"File uploaded: {safe_filename} ({file_size} bytes)")

        if(s3_key and s3_path):
            file_path.unlink()

        return FileUploadResponse(
            filename=safe_filename,
            size=file_size,
            s3_path=s3_path,
            upload_time=datetime.now(),
            status="uploaded"
        )

    except Exception as e:
        logger.error(f"Upload error: {e}")
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=str(e))
