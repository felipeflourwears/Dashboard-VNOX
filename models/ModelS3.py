import boto3
import requests

from io import BytesIO
from .ModelConfig import ModelConfig

class ModelS3:

    def credenciales(self):
        keyS3 = 'AKIAYGSKCJWOE4LDGH3G'
        secretkeyS3 = '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'
        regionS3 = 'us-east-1'
        nameS3 = 'mediapopa'
        return keyS3, secretkeyS3, regionS3, nameS3

    @classmethod
    def upload_media_to_s3(cls, file, media_type, id_player):
        try:
            print("Upload function S3")
            keyS3, secretkeyS3, regionS3, nameS3 = cls().credenciales()
            # Check if the file is not empty
            if file and not file.filename:
                raise ValueError("File is empty or not provided.")
            else:
                print("Archivo con contenido LF")

            print("Content Type: ", file.content_type)

            s3_client = boto3.client(
                's3',
                aws_access_key_id=keyS3,
                aws_secret_access_key=secretkeyS3,
                region_name=regionS3
            )

            # Especifica el parámetro 'Key' en la llamada a put_object
            if media_type == 'image':
                # Extraer la extensión del archivo
                file_extension = file.filename.split('.')[-1].lower()
                # Verificar si la extensión es una imagen compatible
                if file_extension not in ['jpg', 'jpeg', 'png', 'gif']:
                    raise ValueError("Tipo de imagen no compatible.")
                key = f'{id_player}.{file_extension}'
                print(key)
            elif media_type == 'video':
                key = f'{id_player}.mp4'
                print(key)
            else:
                raise ValueError("Tipo de medio no compatible.")

           
            file_data = file.stream.read()

            # Usar BytesIO para garantizar que se trate de datos binarios
            file_stream = BytesIO(file_data)

           # Sube el archivo a S3
            s3_client.put_object(
                Bucket=nameS3,
                Key=key,
                Body=file_stream
            )

            print(f"Archivo {key} subido exitosamente.")

        except Exception as e:
            # Eleva la excepción para que pueda ser manejada externamente
            raise ValueError(f"Error al subir el archivo a AWS S3: {e}")

    @classmethod  
    def media(cls):
        keyS3, secretkeyS3, regionS3, nameS3 = cls().credenciales()
        s3 = boto3.client(
            's3',
            aws_access_key_id=keyS3,
            aws_secret_access_key=secretkeyS3
        )

        bucket_name = nameS3
        response = s3.list_objects_v2(Bucket=bucket_name)
        print(response)

        videos = []
        if 'Contents' in response:
            for obj in response['Contents']:
                if obj['Key'].endswith('.mp4'):
                    name = obj['Key']  # Nombre del video
                    size = obj['Size']  # Tamaño del video
                    videos.append((name, size))

        return videos