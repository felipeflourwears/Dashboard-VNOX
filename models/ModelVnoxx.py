import requests
import json
import time

from .ModelConfig import ModelConfig


class ModelVnoxx():
    @classmethod
    def list_players_vnoxx(cls, db, idCustomer):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT idVnnox, playerId, cliente, tienda, iccid, imsi, msisdn, idCustomer
                     FROM vnoxx
                     WHERE idCustomer = %s"""
            cursor.execute(sql, (idCustomer,))
            rows = cursor.fetchall()

            # Transformar los resultados en un array de diccionarios
            array_list_players = []
            players_selected = []
            for row in rows:
                player = {
                    "idVnnox": row[0],
                    "playerId": row[1],
                    "cliente": row[2],
                    "tienda": row[3],
                    "iccid": row[4],
                    "imsi": row[5],
                    "msisdn": row[6],
                    "idCustomer": row[7]
                }
                array_list_players.append(player)
                players_selected.append(row[1])
            return array_list_players, players_selected
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def getPlayerList_API(cls, token, players_selected):
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
            new_url = f"https://{api_host}{new_api_endpoint}"
            new_headers = {
                'username': username,
                'token': token,
                'Content-Type': 'application/json'
            }

            # Crear una lista para almacenar la información de todos los jugadores
            all_players_info = []

            # Dividir players_selected en lotes de 100
            for i in range(0, len(players_selected), 100):
                batch = players_selected[i:i+100]
                print(f"Procesando batch de {i} a {i+100}, total: {len(batch)}")

                # Modificar la estructura de los datos según el formato deseado
                data = {
                    "playerIds": batch
                }

                # Convertir los datos a formato JSON
                json_data = json.dumps(data)

                while True:
                    # Realizar la nueva solicitud con método POST y los datos en formato JSON
                    new_response = requests.post(new_url, data=json_data, headers=new_headers)
                    # Obtener información sobre la nueva solicitud
                    new_http_code = new_response.status_code
                    print(f"HTTP code: {new_http_code} para batch de {i} a {i+100}")

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
                                all_players_info.append(player_info)
                        break
                    elif new_http_code == 429:
                        print("Rate limit exceeded. Waiting before retrying...")
                        time.sleep(8)  # Esperar 5 segundos antes de reintentar
                    else:
                        print("Error desconocido:", new_http_code)
                        break

            print(f"Total de players_info: {len(all_players_info)}")
            return all_players_info
        else:
            print("Error en la autenticación:", auth_response.status_code)
            return []
        
    @classmethod
    def consumir_api(cls , token, idCustomer):
        url = 'https://retailmibeex.net/apiVnnox/vnnoxService.php?token='
        url += token
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            "idCustomer": idCustomer,
        }
        print("URL: ", url)
        print("TOKEN: ", token)
        print("idCustomer: ", idCustomer)
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Verificar si hubo errores en la respuesta
            
            # Decodificar la respuesta JSON
            data = response.json()
            return data
        
        except requests.exceptions.RequestException as e:
            print(f'Error al realizar la solicitud: {e}')
            return None
