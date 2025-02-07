from dotenv import load_dotenv
import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError

load_dotenv()


class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION"),
        )
        self.bucket_name = os.getenv("AWS_NN_BUCKET_NAME")

    def upload_stream(self, file_stream, s3_key) -> str:
        """
        Uploads a file stream to the specified S3 bucket and returns the S3 URL.
        :param file_stream: The in-memory stream of the file to upload.
        :param s3_key: The key (path/filename) to use for the file in S3.
        :return: The public S3 URL of the uploaded file.
        """
        try:
            self.s3_client.upload_fileobj(file_stream, self.bucket_name, s3_key)
            s3_url = f"https://{self.bucket_name}.s3.amazonaws.com/{s3_key}"
            print(f"File stream uploaded successfully to {s3_url}")
            return s3_url
        except NoCredentialsError:
            raise Exception("AWS credentials not available.")
        except ClientError as e:
            raise Exception(f"Failed to upload file to S3: {e}")

    def download_file(self, s3_key, local_path):
        """
        Downloads a file from the specified S3 bucket.
        :param s3_key: The key (path/filename) in S3 to download.
        :param local_path: The local path where the file should be saved.
        """
        try:
            self.s3_client.download_file(self.bucket_name, s3_key, local_path)
            print(
                f"File '{s3_key}' downloaded successfully from '{self.bucket_name}' to '{local_path}'."
            )
        except NoCredentialsError:
            print("Credentials not available.")
        except ClientError as e:
            print(f"Failed to download file: {e}")

    def delete_file(self, s3_key):
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=s3_key)
        except NoCredentialsError:
            print("Credentials not available.")
        except ClientError as e:
            print(f"Failed to download file: {e}")
