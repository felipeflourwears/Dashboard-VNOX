import requests
import json

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
    print(response.json())
else:
    print("Error en la solicitud:", response.status_code)
    print(response.text)  # Imprime el contenido de la respuesta en caso de error
