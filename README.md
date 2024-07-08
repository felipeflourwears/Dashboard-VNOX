## Access to server
```bash
ssh -i key.pem ubuntu@44.209.129.186
```

### Configure to SSH connections 
```bash
sudo nano /etc/ssh/sshd_config
Enable line -->#Port 22
sudo ufw allow 22/tcp
sudo systemctl restart sshd
sudo systemctl status sshd
sudo ufw app list
```

### Configure Apache
```bash
sudo apt install apache2
sudo ufw app list --->Available applications:
  Apache
  Apache Full
  Apache Secure
  OpenSSH
sudo ufw enable
sudo ufw allow 'Apache'
sudo ufw status --->Output
Status: active
sudo systemctl status apache2

sudo systemctl stop apache2 ------>   Detener apache
sudo systemctl restart apache2 ---> Reiniciar Apache

sudo apt-get install libapache2-mod-wsgi-py3 ---> Module WSGI Apache
```

### Scripts from bashrc
```bash
nano ~/.bashrc
export PATH="$HOME/.local/bin:$PATH"
source ~/.bashrc
```





```bash
import sys
import os

# Ruta al activate_this.py dentro del entorno virtual
activate_this = '/home/ubuntu/.local/share/virtualenvs/webApp-c1qRIGue/bin/activate_this.py'

# Ejecuta activate_this.py para activar el entorno virtual
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Agrega la ruta de tu proyecto al sistema
project_dir = '/var/www/webApp'
if project_dir not in sys.path:
    sys.path.append(project_dir)

# Verifica si el entorno virtual se ha activado
if hasattr(sys, 'real_prefix'):
    print("El entorno virtual se ha activado correctamente.")
else:
    print("¡Advertencia! El entorno virtual no parece estar activado.")

# Importa tu aplicación Flask después de activar el entorno virtual
from app import app as application


```