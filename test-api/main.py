import json
import requests

def get_token():
    # URL del endpoint para enviar la solicitud POST
    url = "https://openapi-us.vnnox.com/v1/oauth/token"
    # Token de autorización para la solicitud POST
    token = "h7vr53"
    # Datos del cuerpo de la solicitud
    data = {
        'username': 'popatelier',
        'password': 'Beex2022.',
    }
    # Encabezados de la solicitud
    headers = {
        'username': 'popatelier',
        'token': token,
        'Content-Type': 'application/json',
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)

    # Comprobar el resultado de la solicitud
    if response.status_code == 200:
        print("Solicitud exitosa!")
        # Extraer el token del JSON de la respuesta
        token_response = response.json().get('data', {}).get('token')
        return token_response
    else:
        print("Error en la solicitud:", response.status_code)
        print(response.text)  # Imprime el contenido de la respuesta en caso de error
        return None  # En caso de error, devuelve None o maneja el error según tus necesidades
    
def use_token(token):
    api_host = 'openapi-us.vnnox.com'
    new_api_endpoint = '/v1/player/getPlayerList'

    username = 'popatelier'
    password = 'Beex2022.'

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
        count_parameter = 1  # El valor que deseas enviar como parámetro count
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

            # Iterar sobre la lista de jugadores
            for player in players_list:
                # Imprimir toda la información de cada jugador
                print("Información del player:")
                for key, value in player.items():
                    print(f"{key}: {value}")

                # Agregar una línea en blanco para separar la información de jugadores
                print("\n")


        else:
            print(f"Error en la nueva solicitud: {new_http_code}")
    else:
        print("Entre al else")
        print(f"Error en la autenticación: {auth_response.status_code}")

# Obtener el token llamando a la función
token = get_token()

# Usar el token según tus necesidades
if token:
    print("Token:", token)
    # Realiza las operaciones que requieran el token aquí
else:
    print("No se pudo obtener el token.")
use_token(token)

