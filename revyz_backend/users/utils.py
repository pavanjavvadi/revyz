import boto3
from django.conf import settings


def aws_conn(service, region):
    aws_conn = boto3.client(
        service,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=region,
    )
    return aws_conn
