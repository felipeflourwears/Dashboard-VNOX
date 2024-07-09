import requests
import urllib3
from datetime import datetime, timedelta

# Desactivar las advertencias de seguridad
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ModelClaroConnect:
    def __init__(self):
        self.username = 'ROBERTO_TERCEROAPI'
        self.password = 'Beex2024%'
        self.base_url = 'https://cc.amx.claroconnect.com:8443/gcapi'
        self.token = None
        self.token_expiration = None

    def authenticate_cc(self):
        # Si ya tenemos un token válido, retornarlo
        if self.token and self.token_expiration > datetime.now():
            return self.token
        
        url = f'{self.base_url}/auth'
        payload = {
            "username": self.username,
            "password": self.password
        }
        headers = {
            'Content-Type': 'application/json'
        }
        try:
            response = requests.post(url, json=payload, headers=headers, verify=False)
            response.raise_for_status()
            data = response.json()
            self.token = data.get('token')
            # Suponiendo que el token expira en 24 horas
            self.token_expiration = datetime.now() + timedelta(hours=24)
            return self.token
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            return None
        except Exception as err:
            print(f'Other error occurred: {err}')
            return None

    @classmethod
    def claroConnectApi(self, imsi, token):
        url = "https://cc.amx.claroconnect.com:8443/gcapi/device/sessionInfo"
        headers = {
            "Authorization": token,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        params = {
            "imsi": imsi
        }
        response = requests.get(url, headers=headers, params=params, verify=False)
        if response.status_code == 200:
            data = response.json()
            self.inSession = data.get('inSession')
            self.sessionStartTime = data.get('sessionStartTime')

            return self.inSession, self.sessionStartTime, data
        else:
            response.raise_for_status()
    
