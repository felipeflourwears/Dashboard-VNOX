import requests

class ModelHexnode:
    
    @classmethod
    def __init__(self, token='YutTIyvOIoQumMDUVkLk'):
        self.token = token

    @classmethod
    def request_data_api(self, idCustomer):
        url = 'https://retailmibeex.net/apiVnnox/hexnodeService.php'
        params = {
            'token': self.token
        }
        payload = {
            "idCustomer": idCustomer,
        }
        try:
            response = requests.get(url, params=params, json=payload)
            response.raise_for_status()  # Verificar si hubo errores en la respuesta

            # Decodificar la respuesta JSON
            data = response.json()

            # Extraer el array de dispositivos
            devices = data.get('Devices', [])
            return devices
        except requests.exceptions.RequestException as e:
            print(f'Error al realizar la solicitud: {e}')
            return None
    
    @classmethod
    def get_devices_summary(self, idCustomer):
        devices = self.request_data_api(idCustomer)
        if devices is None:
            return None, 0, 0, 0

        total = len(devices)
        online = sum(device['compliant'] for device in devices)
        offline = total - online
        return devices, total, online, offline
    