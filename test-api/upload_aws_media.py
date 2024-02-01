import boto3
from dotenv import load_dotenv
import os

load_dotenv()

def upload_media_to_s3(file_path, media_type):
    try:
        s3_client = boto3.client(
            's3',
            aws_access_key_id=os.environ.get('ENV_AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('ENV_AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('ENV_AWS_REGION_NAME')
        )

        with open(file_path, 'rb') as f:
            file_data = f.read()

        # Especifica el parámetro 'Key' en la llamada a put_object
        if media_type == 'image':
            key = 'img_subidalf.png'
        elif media_type == 'video':
            key = 'video_subidolf.mp4'
        else:
            print("Tipo de medio no compatible.")
            return

        s3_client.put_object(
            Bucket=os.environ.get('ENV_AWS_S3_BUCKET_NAME'),
            Key=key,
            Body=file_data
        )

        print(f"Archivo {key} subido exitosamente.")

    except Exception as e:
        print(f"Error: {e}")




image_path = os.path.join(os.path.dirname(__file__), 'img.png')

video_path = os.path.join(os.path.dirname(__file__), 'video.mp4')

# Ejemplo de uso para subir una imagen
upload_media_to_s3(image_path, 'image')

# Ejemplo de uso para subir un video
upload_media_to_s3(video_path, 'video')