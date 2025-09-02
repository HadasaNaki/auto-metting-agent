import boto3
from app.config import settings


class StorageService:
    """Object storage service (S3/MinIO)"""

    def __init__(self):
        self.client = boto3.client(
            "s3",
            endpoint_url=f"http://{settings.minio_endpoint}",
            aws_access_key_id=settings.minio_access_key,
            aws_secret_access_key=settings.minio_secret_key,
        )
        self.bucket = "smartagent-recordings"

    def upload_file(self, file_path: str, object_name: str) -> str:
        """Upload file to storage"""
        try:
            self.client.upload_file(file_path, self.bucket, object_name)
            return f"s3://{self.bucket}/{object_name}"
        except Exception as e:
            raise Exception(f"Upload failed: {str(e)}")

    def download_file(self, object_name: str, file_path: str):
        """Download file from storage"""
        try:
            self.client.download_file(self.bucket, object_name, file_path)
        except Exception as e:
            raise Exception(f"Download failed: {str(e)}")

    def get_presigned_url(self, object_name: str, expiration: int = 3600) -> str:
        """Generate presigned URL for file access"""
        try:
            url = self.client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": object_name},
                ExpiresIn=expiration,
            )
            return url
        except Exception as e:
            raise Exception(f"URL generation failed: {str(e)}")


storage_service = StorageService()
