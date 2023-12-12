import boto3
import os

ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
SECRET_KEY = os.getenv("AWS_SECRET_KEY")
BUCKET = os.getenv("AWS_BUCKET")


def upload_to_bucket(s3_folder_name, local_file_location, image_id):
    client = boto3.client(
        "s3", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET_KEY
    )

    key = f"{s3_folder_name}/{image_id}.png"
    with open(local_file_location, "rb") as image_file:
        client.put_object(
            Bucket=BUCKET,
            Key=key,
            Body=image_file,
            ContentType="image/png",
        )
