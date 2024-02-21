from .entities.Media import Media
import boto3
from io import BytesIO

class ModelS3:
    
    def __init__(self):
        self.s3_client = self.get_s3_client()
        self.bucket_name = self.credenciales()[3]
        self.pagination_limit = 8  # Cantidad de resultados por página

    def credenciales(self):
        keyS3 = 'AKIAYGSKCJWOE4LDGH3G'
        secretkeyS3 = '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'
        regionS3 = 'us-east-1'
        nameS3 = 'mediapopa'
        return keyS3, secretkeyS3, regionS3, nameS3

    def get_s3_client(self):
        keyS3, secretkeyS3, regionS3, nameS3 = self.credenciales()
        return boto3.client(
            's3',
            aws_access_key_id=keyS3,
            aws_secret_access_key=secretkeyS3,
            region_name=regionS3
        )
    

    def upload_file_to_s3(self, file):
        print("Entrando a la función de upload")
        try:
            if not file or not file.filename:
                raise ValueError("File is empty or not provided.")
            
            file_data = file.stream.read()
            file_stream = BytesIO(file_data)

            self.s3_client.upload_fileobj(
                file_stream,
                self.bucket_name,
                file.filename
            )

            print(f"File {file.filename} uploaded successfully.")
        except Exception as e:
            print(f"Error uploading file to S3: {e}")

    def upload_media_to_s3(self, file, media_type, id_player):
        try:
            if not file or not file.filename:
                raise ValueError("File is empty or not provided.")
            
            if media_type == 'image':
                file_extension = file.filename.split('.')[-1].lower()
                if file_extension not in ['jpg', 'jpeg', 'png', 'gif']:
                    raise ValueError("Unsupported image type.")
                key = f'{id_player}.{file_extension}'
            elif media_type == 'video':
                key = f'{id_player}.mp4'
            else:
                raise ValueError("Unsupported media type.")

            file_data = file.stream.read()
            file_stream = BytesIO(file_data)

            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=file_stream
            )

            print(f"File {key} uploaded successfully.")

        except Exception as e:
            raise ValueError(f"Error uploading file to AWS S3: {e}")

    def list_media(self, page_number=1):
        print("Entrando LISTA Busqueda de S3")
        response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
        print(response)
        media = []
        if 'Contents' in response:
            for obj in response['Contents']:
                file_extension = obj['Key'].split('.')[-1].lower()
                if file_extension in ['mp4', 'jpeg', 'jpg', 'png', 'gif']:
                    name = obj['Key']
                    size = obj['Size']
                    lastModified = obj['LastModified']
                    tags = self.get_tags_from_content(name)
                    media.append(
                        Media(id=0, title=name, size=size, lastModified=lastModified, tags=tags)
                    )

        # Ordenar la lista media por lastModified en orden descendente
        media.sort(key=lambda x: x.lastModified, reverse=True)
        
        return media

    def search_media(self, query, page_number=1):
        print("Entrando funcion Busqueda de S3")
        start_index = (page_number - 1) * self.pagination_limit
        end_index = start_index + self.pagination_limit

        response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
        
        media = []
        if 'Contents' in response:
            for obj in response['Contents']:
                file_extension = obj['Key'].split('.')[-1].lower()
                if file_extension in ['mp4', 'gif', 'png', 'jpeg', 'jpg']:
                    name = obj['Key']
                    size = obj['Size']
                    lastModified = obj['LastModified']
                    file_tags = self.get_tags_from_content(name)
                    # Verificar si la consulta coincide con el nombre del archivo o con alguna etiqueta
                    if query.lower() in name.lower() or any(query.lower() in tag.lower() for tag in file_tags):
                        media.append(
                            Media(id=0, title=name, size=size, lastModified=lastModified, tags=file_tags)
                        )

        # Ordenar la lista media por lastModified en orden descendente
        media.sort(key=lambda x: x.lastModified, reverse=True)
        
        return media[start_index:end_index]

    def get_tags_from_content(self, media_name):
        response = self.s3_client.get_object_tagging(
            Bucket=self.bucket_name,
            Key=media_name,
        )
        tagSet = response.get("TagSet")
        if tagSet:
            tagList = [element['Value'] for element in tagSet]
            return tagList
        return []

    def put_tags_to_content(self, media_name, tags):
        tag_list = [{'Key': 'tag', 'Value': tag} for tag in tags]
        response = self.s3_client.put_object_tagging(
            Bucket=self.bucket_name,
            Key=media_name,
            Tagging={'TagSet': tag_list}
        )

    def total_media(self):
        response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)
        total_media = 0
        if 'Contents' in response:
            for obj in response['Contents']:
                file_extension = obj['Key'].split('.')[-1].lower()
                if file_extension in ['mp4', 'gif', 'png', 'jpeg', 'jpg']:
                    total_media += 1
        return total_media
