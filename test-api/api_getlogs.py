import requests
import json

def get_logs(token):
    api_host = 'openapi-us.vnnox.com'
    new_api_endpoint = '/v1/apiLog/GetApiLog'

    username = 'popatelier'

    new_url = f"https://{api_host}{new_api_endpoint}"
    print("URL:", new_url)
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
        print(new_data)

        # Capturar los últimos 3 registros
        last_3_logs = new_data['data']['rows'][-3:]

        # Iterar y mostrar los últimos 3 registros con todos los campos disponibles
        print("\nÚltimos 3 registros:")
        for i, log in enumerate(last_3_logs, start=1):
            print(f"\nRegistro {i}:")
            for key, value in log.items():
                if isinstance(value, dict):
                    print(f"  - {key}:")
                    for sub_key, sub_value in value.items():
                        print(f"    - {sub_key}: {sub_value}")
                else:
                    print(f"  - {key}: {value}")

    else:
        print(f"Error en la nueva solicitud: {new_http_code}")

# Obtener el token llamando a la función
token = 'cc426757f2e3d57e9f91fb12acd92748'
print(token)
get_logs(token)
