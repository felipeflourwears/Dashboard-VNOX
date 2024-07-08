import rsa
import base64
import requests

def get_public_key():
    api_url = "http://esl-eu.zkong.com/zk/user/getErpPublicKey"
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            public_key = data.get('data')  # Obtén el valor de 'data'
            if public_key:
                # Formatea la clave pública en el formato PEM
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

def login_zkong(rsa_encrypted_password):
    account = 'POPOP123'
    url = 'http://esl-eu.zkong.com/zk/user/login' 
    payload = {
        "account": account,
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
        # Devuelve solo el token de la respuesta JSON
        return data.get('data', {}).get('token')
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
        return None
    except Exception as err:
        print(f'Other error occurred: {err}')
        return None

pem_key =  get_public_key()
print("-----------------------------------------------------")
print(pem_key)
print("-----------------------------------------------------")

# Contenido a cifrar
content = "POPOP@123"

# Extraer y decodificar la clave
key_data = ''.join(pem_key.strip().split('\n')[1:-1])
key_bytes = base64.b64decode(key_data)

# Crear un objeto PublicKey de rsa
public_key = rsa.PublicKey.load_pkcs1_openssl_der(key_bytes)

# Cifrar el contenido
encrypted_content = rsa.encrypt(content.encode('utf-8'), public_key)

# Convertir el contenido cifrado a Base64
encrypted_base64 = base64.b64encode(encrypted_content).decode('utf-8')
print("CLAVE RSA:", encrypted_base64)

rsa = encrypted_base64
response = login_zkong(rsa)


