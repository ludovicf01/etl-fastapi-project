"""CSV serve"""
import logging
from typing import Dict, List, Any
import pandas as pd


logger = logging.getLogger(__name__)

class CSVService:
    """CSV file service class"""
    @staticmethod
    def read_csv(file_path: str, nrows: int = None) -> pd.DataFrame:
        """Lire un fichier CSV"""
        try:
            df = pd.read_csv(file_path, nrows=nrows)
            logger.info("CSV read successfully: %s rows", len(df))
            return df
        except Exception as e:
            logger.error("Error reading CSV: %s", e)
            raise

    @staticmethod
    def get_preview(file_path: str, num_rows: int = 5) -> Dict[str, Any]:
        """Obtenir un aperçu du CSV"""
        df = CSVService.read_csv(file_path, nrows=num_rows)
        return {
            "columns": df.columns.tolist(),
            "sample_data": df.to_dict(orient='records'),
            "total_rows": len(df)
        }

    @staticmethod
    def validate_csv(file_path: str) -> Dict[str, Any]:
        """Valider un fichier CSV"""
        try:
            df = pd.read_csv(file_path, nrows=1)
            return {
                "valid": True,
                "columns": df.columns.tolist(),
                "message": "CSV is valid"
            }
        except Exception as e:  # pylint: disable=W0718
            return {
                "valid": False,
                "columns": [],
                "message": str(e)
            }

    @staticmethod
    def clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """Nettoyer les données"""
        # Supprimer les lignes vides
        df = df.dropna(how='all')

        # Supprimer les duplicats
        df = df.drop_duplicates()

        # Nettoyer les espaces
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].str.strip()

        logger.info("Data cleaned: %s rows remaining", len(df))
        return df

    @staticmethod
    def convert_to_records(df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Convertir DataFrame en liste de dictionnaires"""
        return df.to_dict(orient='records')

csv_service = CSVService()
