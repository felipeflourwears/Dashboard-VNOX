import requests

# Datos iniciales
api_host = 'openapi-us.vnnox.com'
username = 'popatelier'
token = '16f5d81a74589ac114ebd2cbc5ddca8f'
api_endpoint = '/v1/player/commandHistory'
url = f"https://{api_host}{api_endpoint}"

# Datos del player
player_id = 'e711e1b488714b0cae07ab873ab42f54'
task_type = 1

# Configurar datos de la solicitud
request_data = {
    'playerId': player_id,
    'taskType': task_type
}

# Configurar encabezado
headers = {
    'username': username,
    'token': token,
    'Content-Type': 'application/json'
}

# Realizar la solicitud HTTP
response = requests.post(url, json=request_data, headers=headers)

# Obtener información sobre la solicitud
http_code = response.status_code

if http_code == 200:
    #print("Acepto 200")
    response_data = response.json()
    print("Response data: ", response_data)

    # Verificar si hay datos en 'rows'
    if 'rows' in response_data['data']:
        rows = response_data['data']['rows']
        print(f"Número de filas: {len(rows)}")

        for row in rows:
            status = row['status']
            execute_time = row['executeTime']
            _type = row['type']
            print(f"Status: {status}, Execute Time: {execute_time}, Type: {_type}")
    else:
        print("No hay datos en 'rows'")
else:
    # Manejar el error según sea necesario
    print(f"Error en la solicitud. Código de estado: {http_code}")
    print("Respuesta:")
    print(response.text)