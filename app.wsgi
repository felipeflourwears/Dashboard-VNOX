import sys
sys.path.insert(0, '/var/www/webApp')

activate_this = '/root/.local/share/virtualenvs/webApp-c1qRIGue/bin/activate_this.py'
with open(activate_this) as file_:
    exect(file.read(), dict(__file__=activate_this))

from app import app as application