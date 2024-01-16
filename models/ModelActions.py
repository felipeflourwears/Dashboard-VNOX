import json
import requests

class ModelActions:
    
    @classmethod  
    def reset_player(self,token, player_id):
        api_host = 'openapi-us.vnnox.com'
        new_api_endpoint = '/v1/player/immediateControl/reboot'

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