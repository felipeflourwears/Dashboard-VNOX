import requests

def use_token():
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

use_token()