## Access to server
```bash
ssh -i key.pem ubuntu@44.209.162.29
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


### Configure AWS Lambda Function

![ProyectFunctionLambda](StartStopWebApp)

To start and stop an EC2 instance, create a function using Python 3.8 with x86 architecture. Adjust permissions in the "Permissions" tab under "Roles" to modify the EC2 instance's status

### Permisiones
![permisions.json](StartStopWebApp/permisions.json)


#### Example basic to init EC2 instance

```bash
import boto3

import json

region = 'us-east-1'

instances = ['i-0a00f85d3a5988589']

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)
    #Change status code ON/OFF
    cont = 0
    if(cont == 0):
        ec2.stop_instances(InstanceIds=instances)
        return {
            'statusCode': 200,
            'body': json.dumps('stopped your instances: ' + str(instances))
        }
    else:
        ec2.start_instances(InstanceIds=instances)
        return {
            'statusCode': 200,
            'body': json.dumps('started your instances: ' + str(instances))
        }

```

### Example to interact with Schedule Server

![Ruta a lambda_function.py](StartStopWebApp/lambda_function.py)

### Expresion Cron
The cron expression that describes the execution of a task from Monday to Friday at 8:35 a.m. and 9:05 p.m. would be as follows:
```bash
cron(35 8,21 ? * MON-FRI *)

```
This expression breaks down as follows:

35 represents the minute (8:35 a.m. and 9:05 p.m.).
8,21 represents the hour (8 a.m. and 9 p.m.).
? is used instead of specifying the day of the month.

for the month (all months).
MON-FRI for the days of the week (Monday to Friday).
Therefore, with this cron expression, the task will run on Mondays to Fridays at 8:35 a.m. and 9:05 p.m.
