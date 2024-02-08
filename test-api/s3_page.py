import boto3

class MediaManager:
    def __init__(self):
        pass

    def credenciales(self):
        # Aquí colocas la lógica para obtener las credenciales de AWS S3
        keyS3 = "AKIAYGSKCJWOE4LDGH3G"
        secretkeyS3 = "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"
        regionS3 = "us-east-1"
        nameS3 = "mediapopa"
        return keyS3, secretkeyS3, regionS3, nameS3

    def media(self, search_term=None, page_size=10, page_number=1):
        keyS3, secretkeyS3, regionS3, nameS3 = self.credenciales()
        s3 = boto3.client(
            's3',
            aws_access_key_id=keyS3,
            aws_secret_access_key=secretkeyS3,
            region_name=regionS3
        )

        bucket_name = nameS3
        videos = []

        # Paginación
        paginator = s3.get_paginator('list_objects_v2')
        paginate_params = {'Bucket': bucket_name}
        if search_term:
            paginate_params['Prefix'] = search_term
        page_iterator = paginator.paginate(**paginate_params)

        for page in page_iterator:
            if 'Contents' in page:
                for obj in page['Contents']:
                    if obj['Key'].endswith('.mp4'):
                        name = obj['Key']  # Nombre del video
                        size = obj['Size']  # Tamaño del video
                        videos.append((name, size))

        # Aplicar filtro de búsqueda si se especificó
        if search_term:
            videos = [video for video in videos if search_term in video[0]]

        # Paginar los resultados según los parámetros proporcionados
        start_index = (page_number - 1) * page_size
        end_index = start_index + page_size
        paginated_videos = videos[start_index:end_index]

        #print("Videos encontrados:", paginated_videos)

        return paginated_videos

# Ejemplo de uso:
media_manager = MediaManager()
videos = media_manager.media(search_term="hot", page_size=20, page_number=1)
for video in videos:
    print(video)