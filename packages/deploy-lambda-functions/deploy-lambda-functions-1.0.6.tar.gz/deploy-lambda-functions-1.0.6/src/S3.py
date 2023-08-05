import boto3
import pathlib
import os
import logging 
from botocore.exceptions import ClientError


class S3Bucket:
    def __init__(self,bucket_name):
        self.bucket_name = bucket_name
        self.client = boto3.client('s3')


    def file_exists(self,file_name):
        try:
            self.client.head_object(Bucket=self.bucket_name,Key=file_name)
        except ClientError as error:
            if error.response["Error"]["Code"] == "404":
                return False
            logging.error(error)
            raise
        return True

    def get_file(self, file_name):
        object = self.client.get_object(Bucket=self.bucket_name,Key=file_name)
        return object["Body"].read().decode('utf-8') 

    def upload_file(self,file_name, object_name=None):
        if not object_name:
            object_name = file_name
        try:
            self.client.upload_file(file_name, self.bucket_name, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def upload_folder(self, input_path, destination_path):
        for root, directories, files in os.walk(input_path, topdown=False):
            for name in files:
                input_file_path = os.path.join(root, name)
                destination_file_path = os.path.join(destination_path,name)
                self.upload_file(input_file_path,destination_file_path)
             
    
    def download_file(self, file_name, download_path=None):
        logging.info("Downloading {} from s3".format(file_name))
        if not download_path:
            download_path = file_name
        download_directory = os.path.dirname(download_path)
        pathlib.Path(download_directory).mkdir(parents=True, exist_ok=True)
        self.client.download_file(self.bucket_name,file_name,download_path)