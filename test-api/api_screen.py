import requests
import json

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

def get_screnn_player(token, player_id):
    api_host = 'openapi-us.vnnox.com'
    new_api_endpoint = '/v1/player/control/screenshot'
    received = 'https://retailmibeex.net/recibe.php'

    username = 'popatelier'
        
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


# Obtener el token llamando a la función
token = get_token()
print(token)

id = "e711e1b488714b0cae07ab873ab42f54"
get_screnn_player(token, id)
