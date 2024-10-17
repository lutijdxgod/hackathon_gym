from contextlib import asynccontextmanager
import logging
from aiobotocore.session import get_session
from botocore.config import Config


class S3Client:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()
        self.botocore_config = Config(
            retries={"max_attempts": 3, "mode": "standard"}, connect_timeout=5, read_timeout=10
        )
        logging.basicConfig(level=logging.INFO)

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self, object, object_name: str):
        async with self.get_client() as client:
            try:
                logging.info(f"Uploading file {object_name} to bucket {self.bucket_name}")
                file_content = await object.read()
                logging.info(f"File {object_name} was succesfully read")
                await client.put_object(Bucket=self.bucket_name, Key=object_name, Body=file_content)
                logging.info(f"Successfully uploaded file {object_name}")
            except Exception as e:
                logging.error(f"Failed to upload file {object_name}: {e}")
                raise

    async def delete_file(self, object_name: str):
        async with self.get_client() as client:
            try:
                logging.info(f"Deleting file {object_name} from bucket {self.bucket_name}")
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
                logging.info(f"Successfully deleted file {object_name}")
            except Exception as e:
                logging.error(f"Failed to delete file {object_name}: {e}")
                raise


# from .config import settings
# import boto3

# s3 = boto3.client("s3")


# async def s3_upload_file(contents, file_name: str):
#     s3.upload_fileobj(contents, settings.bucket_name, file_name)
