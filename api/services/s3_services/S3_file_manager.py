import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os
from dotenv import load_dotenv

class S3FileManager:
    def __init__(self, bucket_name, aws_access_key=None, aws_secret_key=None, region_name=None):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=region_name
        )
        self.bucket_name = bucket_name

    def upload_file(self, file_path, s3_key):
        """
        Uploads a file to the specified S3 bucket.
        :param file_path: The local path of the file to upload.
        :param s3_key: The key (path/filename) to use for the file in S3.
        """
        try:
            self.s3_client.upload_file(file_path, self.bucket_name, s3_key)
            print(f"File '{file_path}' uploaded successfully to '{self.bucket_name}/{s3_key}'.")
        except FileNotFoundError:
            print(f"The file '{file_path}' was not found.")
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

load_dotenv()
base_dir = os.path.dirname(__file__)
file_path = os.path.join(base_dir, 'test.txt')

bucket_name = os.getenv('NN_BUCKET_NAME')
aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('AWS_REGION')

s3_manager = S3FileManager(bucket_name, aws_access_key, aws_secret_key, region_name)

# s3_manager.upload_file(filvx8e_path, 'neural-networks/test.txt')

s3_manager.download_file('test.txt', file_path)
