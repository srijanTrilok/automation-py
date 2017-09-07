import boto3
import logging
import urllib
from .. import config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

glacier_client = boto3.client('glacier')
s3_client = boto3.client('s3')
glacier_bucket = config.glacier_bucket

def upload_glacier(event):
    for file_obj in event['Records']:
        #logger.info(file_obj['s3'])
        key_obj = urllib.unquote_plus(file_obj['s3']['object']['key'].encode("utf8"))
        s3_bucket = file_obj['s3']['bucket']['name']
        #logger.info(key_obj)

        # push file to aws Glacier
        file = s3_client.get_object(Bucket=s3_bucket, Key=key_obj)
        response = glacier_client.upload_archive(
            vaultName=glacier_bucket,
            body=file['Body'].read()
        )

        # now file can be delete
        # need to work on this more
        if(response['archiveId']):
            s3_client.delete_object(Bucket=s3_bucket, Key=key_obj)

        return response;


def download_glacier():
    response = glacier_client.initiate_job(
        vaultName=glacier_bucket,
        jobParameters={'Type': 'inventory-retrieval'}
    )
    return response
