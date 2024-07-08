
import requests
import rsa
import base64

class ModelZkong():
    @classmethod
    def __init__(self, account='POPOP123', password='POPOP@123'):
        self.account = account
        self.password = password
        self.public_key = self.get_public_key()
    
    @classmethod
    def get_public_key(self):
        api_url = "http://esl-eu.zkong.com/zk/user/getErpPublicKey"
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                public_key = data.get('data')
                if public_key:
                    pem_key = f"""
-----BEGIN PUBLIC KEY-----
{public_key}
-----END PUBLIC KEY-----
"""
                    return pem_key
                else:
                    print("Error: 'data' key not found in the response.")
                    return None
            else:
                print(f"Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    @classmethod  
    def encrypt_password(self):
            content = self.password
            key_data = ''.join(self.public_key.strip().split('\n')[1:-1])
            key_bytes = base64.b64decode(key_data)
            public_key = rsa.PublicKey.load_pkcs1_openssl_der(key_bytes)
            encrypted_content = rsa.encrypt(content.encode('utf-8'), public_key)
            encrypted_base64 = base64.b64encode(encrypted_content).decode('utf-8')
            return encrypted_base64
    
    @classmethod
    def login(self):
        rsa_encrypted_password = self.encrypt_password()
        url = 'http://esl-eu.zkong.com/zk/user/login'
        payload = {
            "account": self.account,
            "loginType": 3,
            "password": rsa_encrypted_password
        }
        headers = {
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, json=payload, verify=False)
            response.raise_for_status()
            data = response.json()
            return data.get('data', {}).get('token')
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            return None
        except Exception as err:
            print(f'Other error occurred: {err}')
            return None
        
    @classmethod
    def request_data_api(self, token, idCustomer):
        url = 'https://retailmibeex.net/apiVnnox/zkongService.php?token='
        url += token
        print(token, url)
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            "idCustomer": idCustomer,
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Verificar si hubo errores en la respuesta
            
            # Decodificar la respuesta JSON
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f'Error al realizar la solicitud: {e}')
            return None