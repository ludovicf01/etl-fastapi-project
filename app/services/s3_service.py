"""S3 service"""
import logging
import boto3
from botocore.exceptions import ClientError
from app.config import settings

logger = logging.getLogger(__name__)

class S3Service:
    """S3 service"""
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
            logger.info("Bucket %s exists", self.bucket_name)
        except ClientError:
            try:
                self.s3_client.create_bucket(Bucket=self.bucket_name)
                logger.info("Bucket %s created", self.bucket_name)
            except ClientError as e:
                logger.error("Error creating bucket: %s", e)
                raise

    def upload_file(self, file_path: str, object_name: str) -> str:
        """Upload un fichier vers S3"""
        try:
            self.s3_client.upload_file(file_path, self.bucket_name, object_name)
            logger.info("File %s uploaded to %s", file_path, object_name)
            return f"s3://{self.bucket_name}/{object_name}"
        except ClientError as e:
            logger.error("Error uploading file: %s", e)
            raise

    def download_file(self, object_name: str, file_path: str):
        """Télécharger un fichier depuis S3"""
        try:
            self.s3_client.download_file(self.bucket_name, object_name, file_path)
            logger.info("File %s downloaded to %s", object_name, file_path)
        except ClientError as e:
            logger.error("Error downloading file: %s", e)
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
            logger.error("Error listing files: %s", e)
            raise

    def delete_file(self, object_name: str):
        """Supprimer un fichier de S3"""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=object_name)
            logger.info("File %s deleted", object_name)
        except ClientError as e:
            logger.error("Error deleting file: %s", e)
            raise

s3_service = S3Service()
