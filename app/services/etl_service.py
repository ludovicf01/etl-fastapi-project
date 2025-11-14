from sqlalchemy.orm import Session
from app.models.data import CSVData, OpenDataRecord
from app.services.s3_service import s3_service
from app.services.csv_service import csv_service
import logging
from datetime import datetime
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)

class ETLService:

    @staticmethod
    def process_csv_file(
        db: Session,
        file_path: str,
        filename: str,
        s3_path: str
    ) -> dict:
        """Processus ETL complet pour un fichier CSV"""
        try:
            # 1. Lire le CSV
            df = csv_service.read_csv(file_path)
            original_count = len(df)

            # 2. Nettoyer les données
            df = csv_service.clean_data(df)
            cleaned_count = len(df)

            # 3. Enregistrer les métadonnées
            csv_record = CSVData(
                filename=filename,
                s3_path=s3_path,
                row_count=cleaned_count,
                status="processing"
            )
            db.add(csv_record)
            db.commit()
            db.refresh(csv_record)

            # 4. Insérer en base (exemple avec OpenDataRecord)
            records = []
            for idx, row in df.iterrows():
                # Adapter selon la structure de vos données
                record = OpenDataRecord(
                    code=str(row.get('code', '')),
                    name=str(row.get('name', '')),
                    value=float(row.get('value', 0)) if pd.notna(row.get('value')) else None,
                    category=str(row.get('category', '')),
                    description=str(row.get('description', '')),
                    source_file=filename
                )
                records.append(record)

                # Insertion par batch de 1000
                if len(records) >= 1000:
                    db.bulk_save_objects(records)
                    db.commit()
                    records = []

            # Insérer le reste
            if records:
                db.bulk_save_objects(records)
                db.commit()

            # 5. Mettre à jour le statut
            csv_record.status = "completed"
            db.commit()

            logger.info(f"ETL completed: {cleaned_count} rows inserted")

            return {
                "success": True,
                "filename": filename,
                "original_rows": original_count,
                "cleaned_rows": cleaned_count,
                "inserted_rows": cleaned_count,
                "status": "completed"
            }

        except Exception as e:
            logger.error(f"ETL error: {e}")
            if 'csv_record' in locals():
                csv_record.status = "failed"
                db.commit()
            raise

etl_service = ETLService()
