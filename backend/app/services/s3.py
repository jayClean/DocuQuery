import boto3
from botocore.exceptions import ClientError
from app.config import settings

async def upload_to_s3(file_obj, file_name):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
        region_name=settings.aws_region
    )
    
    try:
        # Ensure to reset the file pointer to the beginning before uploading
        file_obj.seek(0)
        s3_client.upload_fileobj(file_obj, settings.s3_bucket_name, file_name)
    except ClientError as e:
        raise Exception(f"S3 upload failed: {str(e)}")
    
    return f"s3://{settings.s3_bucket_name}/{file_name}"
