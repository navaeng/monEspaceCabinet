import os
from io import BytesIO
from dotenv import load_dotenv
import boto3

load_dotenv()

def get_logo():
    print('obtaining logo from cloud')
    s3_client = boto3.client(
        's3',
        endpoint_url=os.getenv('S3_ENDPOINT'),
        aws_access_key_id=os.getenv('S3_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('S3_SECRET_KEY'),
        region_name="us-west-1"
    )
    print(s3_client.list_buckets()['Buckets'])
    print(f"DEBUG KEY: {os.getenv('S3_ACCESS_KEY')}")
    print(f"DEBUG KEY: {os.getenv('S3_SECRET_KEY')}")
    print(f"DEBUG KEY: {os.getenv('S3_ENDPOINT')}")

    response = s3_client.get_object(Bucket='mybucket', Key='logoNAVA.jpg')
    #
    # img_data = BytesIO(response['Body'].read())
    # img_data.seek(0)
    # return img_data

    content = response['Body'].read()
    print(f"DEBUG IMAGE: {len(content)} bytes, starts with: {content[:10]}")
    img_data = BytesIO(content)
    img_data.seek(0)
    return img_data