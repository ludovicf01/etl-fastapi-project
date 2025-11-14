import boto3
from botocore.exceptions import ClientError
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.S3_REGION
        )
        self.bucket_name = settings.S3_BUCKET_NAME
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Créer le bucket s'il n'existe pas"""
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            logger.info(f"Bucket {self.bucket_name} exists")
        except ClientError:
            try:
                self.s3_client.create_bucket(Bucket=self.bucket_name)
                logger.info(f"Bucket {self.bucket_name} created")
            except ClientError as e:
                logger.error(f"Error creating bucket: {e}")
                raise

    def upload_file(self, file_path: str, object_name: str) -> str:
        """Upload un fichier vers S3"""
        try:
            self.s3_client.upload_file(file_path, self.bucket_name, object_name)
            logger.info(f"File {file_path} uploaded to {object_name}")
            return f"s3://{self.bucket_name}/{object_name}"
        except ClientError as e:
            logger.error(f"Error uploading file: {e}")
            raise

    def download_file(self, object_name: str, file_path: str):
        """Télécharger un fichier depuis S3"""
        try:
            self.s3_client.download_file(self.bucket_name, object_name, file_path)
            logger.info(f"File {object_name} downloaded to {file_path}")
        except ClientError as e:
            logger.error(f"Error downloading file: {e}")
            raise

    def list_files(self, prefix: str = ""):
        """Lister les fichiers dans S3"""
        try:
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            return [obj['Key'] for obj in response.get('Contents', [])]
        except ClientError as e:
            logger.error(f"Error listing files: {e}")
            raise

    def delete_file(self, object_name: str):
        """Supprimer un fichier de S3"""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_name)
            logger.info(f"File {object_name} deleted")
        except ClientError as e:
            logger.error(f"Error deleting file: {e}")
            raise

s3_service = S3Service()
