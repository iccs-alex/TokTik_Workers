import boto3
import os


s3Client = boto3.client('s3', 
                        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'), 
                        aws_secret_access_key=os.getenv('AWS_ACCESS_KEY_SECRET')
                        )


def getVideo(videoKey: str):
    print("Getting video")
    response = s3Client.get_object(Bucket='toktik-videos', Key=f'mp4/{videoKey}')
    print("Got video")
    return response


def putVideo(videoKey, filepath):
    response = s3Client.upload_file(filepath, "toktik-videos", videoKey)
    return response
