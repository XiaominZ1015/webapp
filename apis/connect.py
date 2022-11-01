import boto3
import pathlib
import os

from apis.version1.authenticated import get_bucket_name


def upload_file_using_resource(fileName: str):
    """
    Uploads file to S3 bucket using S3 resource object.
    This is useful when you are dealing with multiple buckets st same time.
    :return: None
    """
    s3 = boto3.resource("s3")
    bucket_name = get_bucket_name()
    object_name = fileName
    file_name = os.path.join(pathlib.Path(
        __file__).parent.resolve(), fileName)
    bucket = s3.Bucket(bucket_name)
    response = bucket.upload_file(file_name, object_name)


def delete_file_using_resource():
    return