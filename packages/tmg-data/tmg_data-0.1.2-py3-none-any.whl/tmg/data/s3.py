import boto3
import botocore
import os
import parse
import sys
from tmg.data import logs


class Client:
    """
        Client to s3 Storage functionality.

        Args:
            connection_string (str): The S3 connection string in the format
                                     {region}:{access_key}:{secret_key}
    """

    def __init__(self, connection_string):
        parsed_connection = parse.parse('{region}:{access_key}:{secret_key}', connection_string)
        self.s3_client = boto3.resource(service_name='s3',
                                        region_name=parsed_connection['region'],
                                        aws_access_key_id=parsed_connection['access_key'],
                                        aws_secret_access_key=parsed_connection['secret_key'])

    def download(self, bucket_name, object_name, local_path='.'):
        """
        Downloads a file from the s3 to the local system.

        Args:
            bucket_name (str): s3 bucket name
            object_name (str): s3 file name to download
            local_path (str): local file name with path. If local path is a directory
                              object name is used as local file name

        Example:
            >>> from tmg.data import s3
            >>> client = s3.Client('region:access_key:secret_key')
            >>> client.download(bucket_name='my-s3-bucket-name',
            >>>                 object_name='folder-name/object-name',
            >>>                 local_path='/my-local/folder/file.csv')
        """
        if os.path.isdir(local_path):
            filename = os.path.basename(object_name)
            local_path = os.path.join(local_path, filename)

        try:
            logs.client.logger.info(f"Starting {os.path.basename(object_name)} download from {bucket_name} s3 bucket")
            bucket = self.s3_client.Bucket(bucket_name)
            bucket.download_file(object_name, local_path)
        except botocore.exceptions.ClientError as e:
            logs.client.logger.error(f"The file {os.path.basename(object_name)} doesn't exists in the bucket, Terminating")
            sys.exit(1)

        logs.client.logger.info("File download completed")

    def upload(self, local_path, bucket_name, object_name=None):
        """
        Uploads a local file to s3 bucket

        Args:
            local_path (str): File with path to upload
            bucket_name (str): s3 bucket name
            object_name (str): S3 object name. If not specified then local file_name is used

        Example:
            >>> from tmg.data import s3
            >>> client = s3.Client('region:access_key:secret_key')
            >>> client.upload(local_path='/my-local/folder/file.csv',
            >>>               bucket_name='my-s3-bucket-name',
            >>>               object_name='object-name')
        """

        if object_name is None:
            object_name = os.path.basename(local_path)

        logs.client.logger.info(f"Starting {os.path.basename(local_path)} upload to {bucket_name} s3 bucket")
        bucket = self.s3_client.Bucket(bucket_name)
        bucket.upload_file(local_path, object_name)
        logs.client.logger.info("File upload completed")
