import requests
import json
import hashlib

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
            count_parameter = 2  # El valor que deseas enviar como parámetro count
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
    def upload_media_player(self, token, player_id, link):
        api_host = 'openapi-us.vnnox.com'
        new_api_endpoint = '/v1/player/program/normal'

        username = ModelConfig.username_auth()
            
        new_url = f"https://{api_host}{new_api_endpoint}"
        print("URLlf:", new_url)
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
            print("Es un video")
        elif link.endswith(('.jpg', '.png', '.jpeg', '.gif')):
            typemedia = "PICTURE"
            print("Es una imagen")
        else:
            print("Extensión de archivo no compatible")

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
        received = 'https://retailmibeex.net/apiVnnox/recibe.php'
        print("Entrando a funcion get_screen_shot")

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
        print("Response Screen: ",new_response)

        # Obtener información sobre la nueva solicitud
        new_http_code = new_response.status_code

        # Manejar la respuesta de la nueva solicitud
        if new_http_code == 200:
            # La solicitud fue exitosa (código de estado 200)
            # Decodificar la respuesta JSON de la nueva API
            new_data = new_response.json()
            print("Response Screen: ",new_data)
        else:
            print(f"Error en la nueva solicitud: {new_http_code}")
    
    @classmethod 
    def get_logs(self, token):
        api_host = 'openapi-us.vnnox.com'
        new_api_endpoint = '/v1/apiLog/GetApiLog'

        username = 'popatelier'

        new_url = f"https://{api_host}{new_api_endpoint}"
        headers = {
            'username': username,
            'token': token,
            'Content-Type': 'application/json'
        }

        request_parameters = {}

        new_response = requests.get(new_url, headers=headers, json=request_parameters)
        print(new_response)

        new_http_code = new_response.status_code

        if new_http_code == 200:
            new_data = new_response.json()
            #print(new_data)

            # Capturar los últimos 3 registros
            last_3_logs = new_data['data']['rows'][-3:]

            # Iterar y mostrar los últimos 3 registros con todos los campos disponibles
            return last_3_logs

        else:
            print(f"Error en la nueva solicitud: {new_http_code}")
            return []
    
    @classmethod 
    def getPlayerList_Selected(self, token):
        api_host = 'openapi-us.vnnox.com'
        new_api_endpoint = '/v1/player/get/syncCurrentInfo'

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

        if auth_response.status_code == 200:
            
            #players_selected = ['e711e1b488714b0cae07ab873ab42f54', 'cba03d3e4372481cbbdf177ffbb213b6']
            players_selected = ['c7171e192368d1af8e259f2874c21d4c', '12b7cb332b4582cd342763cf0929ff16']
            new_url = f"https://{api_host}{new_api_endpoint}"
            new_headers = {
                'username': username,
                'token': token,
                'Content-Type': 'application/json'
            }

            # Modificar la estructura de los datos según el formato deseado
            data = {
                "playerIds": players_selected
            }

            # Convertir los datos a formato JSON
            json_data = json.dumps(data)

            # Realizar la nueva solicitud con método POST y los datos en formato JSON
            new_response = requests.post(new_url, data=json_data, headers=new_headers)
            # Obtener información sobre la nueva solicitud
            new_http_code = new_response.status_code

            # Crear una lista para almacenar la información
            players_info = []

            # Manejar la respuesta de la nueva solicitud
            if new_http_code == 200:
                # Decodificar la respuesta JSON de la nueva API
                new_data = new_response.json()
                if 'data' in new_data:
                    for player in new_data['data']:
                        player_info = {
                            'playerId': player.get('playerId'),
                            'playerType': player.get('playerType'),
                            'name': player.get('name'),
                            'sn': player.get('sn'),
                            'version': player.get('version'),
                            'ip': player.get('ip'),
                            'productName': player.get('productName'),
                            'onlineStatus': player.get('onlineStatus'),
                            'lastOnlineTime': player.get('lastOnlineTime')
                        }
                        players_info.append(player_info)
            return players_info
        else:
            print("Error en la autenticación:", auth_response.status_code)


