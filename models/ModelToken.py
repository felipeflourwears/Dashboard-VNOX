import json
import requests

from .ModelConfig import ModelConfig


class ModelToken:
    
    @classmethod  
    def get_token(self):
        # URL del endpoint para enviar la solicitud POST
        url = "https://openapi-us.vnnox.com/v1/oauth/token"
        # Token de autorización para la solicitud POST
        token = ModelConfig.token_auth()
        username = ModelConfig.username_auth()
        passw = ModelConfig.pass_username()
        # Datos del cuerpo de la solicitud
        data = {
            'username': username,
            'password': passw,
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
    
    