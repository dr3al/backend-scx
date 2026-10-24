import boto3
from botocore.exceptions import ClientError, BotoCoreError
from fastapi import HTTPException

from adapters.file_storage.base import FileStorageAdapter

class S3FileStorageAdapter(FileStorageAdapter):
    def __init__(
        self,
        bucket_name: str,
        access_key: str,
        secret_key: str,
        region_name: str = "ru-central1",
        url: str = "https://storage.yandexcloud.net",
    ):
        self.bucket_name = bucket_name
        self.url = url
        self.client = boto3.client(
            "s3",
            endpoint_url=url,
            region_name=region_name,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )
    def upload_file(self, key: str, data: bytes):
        try:
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=data,
                ContentType="application/octet-stream",
            )
        except (ClientError, BotoCoreError) as e:
            raise HTTPException(status_code=404, detail=str(e))

        return f"{self.url}/{self.bucket_name}/{key}"

# Для проверки записи
if __name__ == "__main__":
    s3 = S3FileStorageAdapter(
        bucket_name="",
        access_key="",
        secret_key="",
    )

    s3.upload_file("hello.txt", b"Hello, World!")