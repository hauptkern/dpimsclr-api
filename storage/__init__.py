import boto3
from core.config import settings

s3 = boto3.client('s3',
                  endpoint_url=settings.S3_ENDPOINT_URL,
                  use_ssl=False,
                  aws_access_key_id=settings.S3_ACCESS_KEY,
                  aws_secret_access_key=settings.S3_SECRET_KEY
                  )
