import boto3
import logging
import os, sys
from botocore.exceptions import ClientError

BOTO_KWARGS = {
    "aws_access_key_id": os.getenv('AWS_ACCESS_KEY_ID'),
    "aws_secret_access_key": os.getenv('AWS_SECRET_ACCESS_KEY'),
    "region_name": os.getenv('AWS_REGION_NAME'),
}
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

class AWS_Hook():
    def __init__(self):
        pass

    @staticmethod
    def construct_url(filename):
        s3_client = boto3.Session(**BOTO_KWARGS).client("s3")
        location = s3_client.get_bucket_location(Bucket=S3_BUCKET_NAME)['LocationConstraint']
        if not location or location is None:
            location = BOTO_KWARGS['region_name']
        url = "https://s3.%s.amazonaws.com/%s/%s" % (location, S3_BUCKET_NAME, filename)
        return url

    @staticmethod
    def upload_file(local_folder,bucket_folder,file_name, new_filename = False):
        """Upload a file to an S3 bucket
        :param file_name: File to upload
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        
        # Upload the file
        s3_client = boto3.Session(**BOTO_KWARGS).client("s3")
        if not new_filename:
            new_filename = file_name
        try:
            response = s3_client.upload_file(local_folder+"/"+file_name, S3_BUCKET_NAME, bucket_folder+new_filename)
            print (response)
        except ClientError as e:
            logging.error(e)
            return False
        print (response)
        return True
