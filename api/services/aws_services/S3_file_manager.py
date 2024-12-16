import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os
from dotenv import load_dotenv
from io import BytesIO

class S3FileManager:
    def __init__(self, bucket_name, aws_access_key=None, aws_secret_key=None, region_name=None):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name
        )
        self.bucket_name = bucket_name

    def upload_stream(self, file_stream, s3_key):
        """
        Uploads a file stream to the specified S3 bucket.
        :param file_stream: The in-memory stream of the file to upload.
        :param s3_key: The key (path/filename) to use for the file in S3.
        """
        try:
            self.s3_client.upload_fileobj(file_stream, self.bucket_name, s3_key)
            print(f"File stream uploaded successfully to '{self.bucket_name}/{s3_key}'.")
        except NoCredentialsError:
            print("Credentials not available.")
        except ClientError as e:
            print(f"Failed to upload file: {e}")

    def download_file(self, s3_key, local_path):
        """
        Downloads a file from the specified S3 bucket.
        :param s3_key: The key (path/filename) in S3 to download.
        :param local_path: The local path where the file should be saved.
        """
        try:
            self.s3_client.download_file(self.bucket_name, s3_key, local_path)
            print(f"File '{s3_key}' downloaded successfully from '{self.bucket_name}' to '{local_path}'.")
        except NoCredentialsError:
            print("Credentials not available.")
        except ClientError as e:
            print(f"Failed to download file: {e}")
