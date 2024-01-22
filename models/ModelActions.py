import json
import requests
import boto3
import os
import hashlib

from werkzeug.utils import secure_filename
from .ModelConfig import ModelConfig

class ModelActions:
    
    @classmethod  
    def reset_player(self,token, player_id):
        api_host = 'openapi-us.vnnox.com'
        new_api_endpoint = '/v1/player/immediateControl/reboot'

        username = ModelConfig.username_auth()
            
        new_url = f"https://{api_host}{new_api_endpoint}"
        print("URL:", new_url)
        headers = {
            'username': username,
            'token': token,
            'Content-Type': 'application/json'  # Asegúrate de incluir el tipo de contenido JSON en los headers
        }

        # Parámetros a enviar en el cuerpo de la solicitud
        request_parameters = {
            "playerIds": [player_id]  # Nota: es posible que la API espere una lista de IDs
        }

        # Realizar la nueva solicitud con método POST
        new_response = requests.post(new_url, headers=headers, json=request_parameters)
        print(new_response)

        # Obtener información sobre la nueva solicitud
        new_http_code = new_response.status_code

        # Manejar la respuesta de la nueva solicitud
        if new_http_code == 200:
            # La solicitud fue exitosa (código de estado 200)
            # Decodificar la respuesta JSON de la nueva API
            new_data = new_response.json()
            print(new_data)
        else:
            print(f"Error en la nueva solicitud: {new_http_code}")
   
    @classmethod  
    def getPlayerList(self, token):
        api_host = 'openapi-us.vnnox.com'
        new_api_endpoint = '/v1/player/getPlayerList'

        username = ModelConfig.username_auth()
        password = ModelConfig.pass_username()

        # Solicitud de autenticación para obtener el token
        auth_url = f"https://{api_host}/v1/oauth/token"
        auth_payload = {
            'username': username,
            'password': password,
            'grant_type': 'password'
        }

        auth_response = requests.post(auth_url, data=auth_payload)


        # Verificar si la autenticación fue exitosa (código de estado 200)
        if auth_response.status_code == 200:
            # Utilizar el token fijo (modifica según tus necesidades)
            #token = 'd1aeb85c5c2f78dbf2c09fc9922fce77'

            # Nueva URL y encabezados para la siguiente solicitud
            start_parameter = 0
            #start_parameter = 287
            count_parameter = 5  # El valor que deseas enviar como parámetro count
            new_url = f"https://{api_host}{new_api_endpoint}?count={count_parameter}&start={start_parameter}"
            new_headers = {
                'username': username,
                'token': token
            }

            # Realizar la nueva solicitud con método GET
            new_response = requests.get(new_url, headers=new_headers)
            #print(new_response.text)


            # Obtener información sobre la nueva solicitud
            new_http_code = new_response.status_code

            # Inicializar la lista de nombres de jugadores
            names_players_list = []

            # Manejar la respuesta de la nueva solicitud
            if new_http_code == 200:
                # La solicitud fue exitosa (código de estado 200)

                # Decodificar la respuesta JSON de la nueva API
                new_data = new_response.json()

                # Obtener la lista de jugadores
                players_list = new_data['data']['rows']

                # Crear una lista para almacenar la información de los jugadores
                players_info = []

                # Iterar sobre la lista de jugadores
                for player in players_list:
                    # Crear un diccionario para almacenar la información de cada jugador
                    player_info = {}

                    # Iterar sobre las claves y valores de cada jugador
                    for key, value in player.items():
                        # Agregar la información al diccionario del jugador
                        player_info[key] = value

                    # Agregar el diccionario del jugador a la lista de players_info
                    players_info.append(player_info)

                # Imprimir la información de los jugadores almacenada en la lista
                """ for player_info in players_info:
                    print("Información del jugador:")
                    for key, value in player_info.items():
                        print(f"{key}: {value}")"""
                    #print("\n")

                return players_info 
            else:
                print(f"Error en la nueva solicitud: {new_http_code}")
        else:
            print("Entre al else")
            print(f"Error en la autenticación: {auth_response.status_code}")

    @classmethod 
    def upload_media_player(self, token, player_id):
        api_host = 'openapi-us.vnnox.com'
        new_api_endpoint = '/v1/player/program/normal'

        username = ModelConfig.username_auth()
            
        new_url = f"https://{api_host}{new_api_endpoint}"
        print("URL:", new_url)
        headers = {
            'username': username,
            'token': token,
            'Content-Type': 'application/json'  # Asegúrate de incluir el tipo de contenido JSON en los headers
        }

        # Parámetros a enviar en el cuerpo de la solicitud
        request_parameters = {
            "playerIds": [
                "13630ecc0741dd8246483c89bec9be6e"
            ],
            "pages":[
                {
                    "name":"a-page",
                    "widgets":[
                        {
                            "zIndex":1,
                            "type":"PICTURE",
                            "size":1022978, 
                            "md5":"0c80b5deb89d607133d445181730ff1d",
                            "duration":10000,
                            "url":"https://retailmibeex.net/images/cafe2.png",
                            "layout":{
                                "x":"0%",
                                "y":"0%",
                                "width":"100%",
                                "height":"100%"
                            },
                            "inAnimation":{
                                "type":"NONE",
                                "duration":1000
                            }
                        }
                    ]
                }
            ]
        }
        # Realizar la nueva solicitud con método POST
        new_response = requests.post(new_url, headers=headers, json=request_parameters)
        print(new_response)

        # Obtener información sobre la nueva solicitud
        new_http_code = new_response.status_code

        # Manejar la respuesta de la nueva solicitud
        if new_http_code == 200:
            # La solicitud fue exitosa (código de estado 200)
            # Decodificar la respuesta JSON de la nueva API
            new_data = new_response.json()
            print(new_data)
        else:
            print(f"Error en la nueva solicitud: {new_http_code}")
    
    @classmethod 
    def send_report(self):
        # Solicitud de autenticación para obtener el token
        auth_url = "https://retailmibeex.net/email.php"
        auth_payload = {}

        # Realizar la solicitud
        response = requests.get(auth_url, data=auth_payload)

        # Verificar el código de estado HTTP
        print(response)
        if response.status_code == 200:
            print("Exitoso")
        else:
            print(f"Error en la nueva solicitud. Código de estado: {response.status_code}")

    @classmethod
    def upload_media_to_s3(self, file, media_type, id_player):
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=os.environ.get('ENV_AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.environ.get('ENV_AWS_SECRET_ACCESS_KEY'),
                region_name=os.environ.get('ENV_AWS_REGION_NAME')
            )

            # Obtener el nombre de archivo seguro
            filename = secure_filename(file.filename)

            # Especifica el parámetro 'Key' en la llamada a put_object
            if media_type == 'image':
                key = f'{id_player}.png'
            elif media_type == 'video':
                key = f'{id_player}.mp4'
            else:
                raise ValueError("Tipo de medio no compatible.")

            # Lee los datos del archivo
            file_data = file.read()

            # Sube el archivo a S3
            s3_client.put_object(
                Bucket=os.environ.get('ENV_AWS_S3_BUCKET_NAME'),
                Key=key,
                Body=file_data
            )

            print(f"Archivo {key} subido exitosamente.")

        except Exception as e:
            # Eleva la excepción para que pueda ser manejada externamente
            raise ValueError(f"Error al subir el archivo a AWS S3: {e}")
    
    @classmethod      
    def upload_media_player(self, token, player_id, link):
        api_host = 'openapi-us.vnnox.com'
        new_api_endpoint = '/v1/player/program/normal'

        username = ModelConfig.username_auth()
            
        new_url = f"https://{api_host}{new_api_endpoint}"
        print("URL:", new_url)
        headers = {
            'username': username,
            'token': token,
            'Content-Type': 'application/json'  # Asegúrate de incluir el tipo de contenido JSON en los headers
        }

        response = requests.head(link)
        file_size = int(response.headers.get('content-length', 0))

        # Descargar el archivo
        response_url = requests.get(link)
        content = response_url.content

        # Calcular el hash MD5
        md5_hash = hashlib.md5(content).hexdigest()

        # Validar el tipo de medio según la extensión del enlace
        if link.endswith('.mp4'):
            typemedia = "VIDEO"
        elif link.endswith(('.jpg', '.png', '.jpeg')):
            typemedia = "PICTURE"
        else:
            print("Extensión de archivo no compatible")
            return

        # Parámetros a enviar en el cuerpo de la solicitud
        if typemedia=="PICTURE":
            request_parameters = {
                "playerIds": [
                    player_id
                ],
                "pages":[
                    {
                        "name":"a-page",
                        "widgets":[
                            {
                                "zIndex":1,
                                "type":"PICTURE",
                                "size": file_size,
                                "md5": md5_hash,
                                "duration":10000,
                                "url": link,
                                "layout":{
                                    "x":"0%",
                                    "y":"0%",
                                    "width":"100%",
                                    "height":"100%"
                                },
                                "inAnimation":{
                                    "type":"NONE",
                                    "duration":1000
                                }
                            }
                        ]
                    }
                ]
            }
        else:
            request_parameters = {
                "playerIds": [
                    player_id
                ],
                "pages":[
                    {
                        "name":"a-page",
                        "widgets":[
                                {
                                "zIndex":2,
                                "type":"VIDEO",
                                "size": file_size,
                                "md5": md5_hash,
                                "duration":0,
                                "url": link,
                                "layout":{
                                    "x":"0%",
                                    "y":"0%",
                                    "width":"100%",
                                    "height":"100%"
                                }
                            }
                        ]
                    }
                ]
            }
        # Realizar la nueva solicitud con método POST
        new_response = requests.post(new_url, headers=headers, json=request_parameters)
        print(new_response)

        # Obtener información sobre la nueva solicitud
        new_http_code = new_response.status_code

        # Manejar la respuesta de la nueva solicitud
        if new_http_code == 200:
            # La solicitud fue exitosa (código de estado 200)
            # Decodificar la respuesta JSON de la nueva API
            new_data = new_response.json()
            print("Upload Success Player:", new_data)
        else:
            print(f"Error en la nueva solicitud: {new_http_code}")

    @classmethod      
    def get_screnn_player(self, token, player_id):
        api_host = 'openapi-us.vnnox.com'
        new_api_endpoint = '/v1/player/control/screenshot'
        received = 'https://retailmibeex.net/recibe.php'

        username = ModelConfig.username_auth()
            
        new_url = f"https://{api_host}{new_api_endpoint}"
        print("URL:", new_url)
        headers = {
            'username': username,
            'token': token,
            'Content-Type': 'application/json'  # Asegúrate de incluir el tipo de contenido JSON en los headers
        }

        # Parámetros a enviar en el cuerpo de la solicitud
        request_parameters = {
            "playerIds": [player_id],
            "noticeUrl": received
        }

        # Realizar la nueva solicitud con método POST
        new_response = requests.post(new_url, headers=headers, json=request_parameters)
        print(new_response)

        # Obtener información sobre la nueva solicitud
        new_http_code = new_response.status_code

        # Manejar la respuesta de la nueva solicitud
        if new_http_code == 200:
            # La solicitud fue exitosa (código de estado 200)
            # Decodificar la respuesta JSON de la nueva API
            new_data = new_response.json()
            print(new_data)
        else:
            print(f"Error en la nueva solicitud: {new_http_code}")

    @classmethod      
    def upload_media_player_simulate(self, token, player_id, temp):
        temperature_variant = int(temp)
        api_host = 'openapi-us.vnnox.com'
        new_api_endpoint = '/v1/player/program/normal'

        username = ModelConfig.username_auth()
            
        new_url = f"https://{api_host}{new_api_endpoint}"
        print("URL:", new_url)
        headers = {
            'username': username,
            'token': token,
            'Content-Type': 'application/json'  # Asegúrate de incluir el tipo de contenido JSON en los headers
        }

        if temperature_variant > 0:
            request_parameters = {
                    "playerIds": [
                        player_id
                    ],
                    "pages":[
                    {
                        "name":"a-page",
                        "widgets":[
                            {
                            "zIndex":2,
                            "type":"VIDEO",
                            "size": 23507832,
                            "md5": "b353959bad9d2b3decefeeeed60f6546",
                            "duration":0,
                            "url": "https://mediapopa.s3.amazonaws.com/hot.mp4",
                                "layout":{
                                    "x":"0%",
                                    "y":"0%",
                                    "width":"100%",
                                    "height":"100%"
                                }
                            }
                        ]
                    }
                ]
            }
        else: 
            request_parameters = {
                    "playerIds": [
                        player_id
                    ],
                    "pages":[
                    {
                        "name":"a-page",
                        "widgets":[
                            {
                            "zIndex":2,
                            "type":"VIDEO",
                            "size": 24440147,
                            "md5": "c156cf0dac971ae49dd5668b345f7fc0",
                            "duration":0,
                            "url": "https://mediapopa.s3.amazonaws.com/frio.mp4",
                                "layout":{
                                    "x":"0%",
                                    "y":"0%",
                                    "width":"100%",
                                    "height":"100%"
                                }
                            }
                        ]
                    }
                ]
            }
        # Realizar la nueva solicitud con método POST
        new_response = requests.post(new_url, headers=headers, json=request_parameters)
        print(new_response)

        # Obtener información sobre la nueva solicitud
        new_http_code = new_response.status_code

        # Manejar la respuesta de la nueva solicitud
        if new_http_code == 200:
            # La solicitud fue exitosa (código de estado 200)
            # Decodificar la respuesta JSON de la nueva API
            new_data = new_response.json()
            print("Upload Success Player:", new_data)
        else:
            print(f"Error en la nueva solicitud: {new_http_code}")
