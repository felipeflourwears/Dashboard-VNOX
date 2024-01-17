import hashlib
import requests

#url = "https://mediapopa.s3.amazonaws.com/main.mp4"
#url ="https://retailmibeex.net/images/cafe2.png"
url="https://retailmibeex.net/images/main.mp4"
url = "https://mediapopa.s3.amazonaws.com/test.mp4"

# Descargar el archivo
response = requests.get(url)
content = response.content

# Calcular el hash MD5
md5_hash = hashlib.md5(content).hexdigest()

print(f"MD5 Hash: {md5_hash}")
