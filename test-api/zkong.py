import rsa
import base64

# Contenido de la clave pública PEM
pem_key = """
-----BEGIN RSA PRIVATE KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC8QJoimmV5xW1ht2Sh0I7GADk8
/h/rWF5mXODsz5HaAH4c0+GdSnZcYZNbVhkZk+WG+fTwksJb6cQOJrVmbm6K0Hr/
Iqjv/wx9zZCD6TbmB/RZ3Bas606NIboOysgI6iURBsXJrUzcGWZNHVfITaYtIZer
W63aDPaepn55QsSyIwIDAQAB
-----END RSA PRIVATE KEY-----
"""

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