from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort, make_response

#Instances Models
from models.ModelToken import ModelToken
from models.ModelActions import ModelActions
from models.ModelUser import ModelUser
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from config import config
from config import Config

#Entities
from models.entities.User import User

import time
import os
import string
import random
import pdfkit
import base64
import datetime

#Import to manage tokens to authenticate
from flask_wtf.csrf import CSRFProtect
from flask_mysqldb import MySQL

#Import to manage control with LOGIN
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

# Variables globales para almacenar el token y su tiempo de expiración
token_info = {
    'token': None,
    'expiration_time': 0
}

app = Flask(__name__)
app.config.from_object(Config)  # Configura la aplicación con la clase de configuración

config_instance = Config()  # Crea una instancia de la clase Config
config_instance.print_secret_key()  #
model_token = ModelToken() 
model_actions = ModelActions()
db = MySQL(app)

load_dotenv()
login_manager_app = LoginManager(app)
csrf = CSRFProtect(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4'}

token = 'c496d057e92312f83ddca988dc6eb3fe'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def obtener_token():
    print("Entrando a la funcion OT")
    current_time = time.time()

    # Verificar si el token existente sigue siendo válido
    if token_info['token'] is None or current_time > token_info['expiration_time']:
        # Obtener un nuevo token si no hay uno existente o ha expirado
        new_token = ModelToken.get_token()
        token_info['token'] = new_token
        # Establecer el tiempo de expiración (ajusta según sea necesario)
        token_info['expiration_time'] = current_time + 86000
        print("NEW TOKEN")
        print("token: ", token_info)
        return token_info['token']
    else:
        print("ELSE TODAVIA MISMO TOKEN")
        print("token: ", token_info)
        return token_info['token']
    
@app.route('/reset_player/<string:player_id>', methods=['GET'])
def reset_player(player_id):
    try:
        #token = obtener_token()
        print(f"Token: {token}")
        
        ModelActions.reset_player(token, player_id)
        print(f"Player reset successfully: {player_id}")

        # Redirigir al usuario a la ruta principal después de resetear el player
        return redirect(url_for('index', reset='reset'))
    except Exception as e:
        print(f"Error resetting player: {str(e)}")
        # Aquí puedes agregar un manejo más específico del error si es necesario
        return render_template('404.html', error_message=str(e))
    

@app.route('/send_report')
def send_report():
    try:
        ModelActions.send_report()
        # Redirigir al usuario a la ruta principal después de resetear el player
        print("Dentro del try")
        return redirect(url_for('index', sendreport='sendreport'))
    except Exception as e:
        print(f"Error resetting player: {str(e)}")
        # Aquí puedes agregar un manejo más específico del error si es necesario
        return render_template('404.html', error_message=str(e))

@app.route('/edit_player/')
def edit_player():
    # Obtener los parámetros de la URL
    get_logs = ModelActions.get_logs(token)
    player_id = request.args.get('player_id')
    ip = request.args.get('ip')
    name = request.args.get('name')
    
    # Generar una cadena aleatoria para evitar el almacenamiento en caché
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    #token = obtener_token()
    #token = '0ce1973ddb9a293cf177e3626135078a'
    ModelActions.get_screnn_player(token, player_id)
    
    # Imprimir los valores (puedes eliminar esto en producción)
    print(f"Player ID: {player_id}, IP: {ip}, Name: {name}")
    
    # Renderizar la plantilla con los valores y la cadena aleatoria
    return render_template('edit-player.html', player_id=player_id, ip=ip, name=name, random_string=random_string, get_logs=get_logs)

@app.route('/submit_form_media', methods=['POST'])
def submit_form_media():
    player_id = request.form.get('playerId')
    if 'imageUpload' in request.files:
        file = request.files['imageUpload']
        print(file)
        
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                print("Filename: ", filename)
                media_type = 'image' if filename.lower().endswith(('.png', '.jpg', '.jpeg')) else 'video'
                print("Type: ", media_type)
                
                # Utiliza la función de carga a S3
                ModelActions.upload_media_to_s3(file, media_type, player_id)
                
                if media_type == 'image':
                    # Obtener la extensión de la imagen
                    extension = filename.split('.')[-1].lower()
                    # Crear el enlace dinámico para imágenes
                    link = f'https://mediapopa.s3.amazonaws.com/{player_id}.{extension}'
                else:
                    # Enlace para videos
                    link = f'https://mediapopa.s3.amazonaws.com/{player_id}.mp4'

                print("URL: ", link)
                
                #token = obtener_token()  # Asegúrate de tener definida la función obtener_token()
                #token = '0ce1973ddb9a293cf177e3626135078a'
                ModelActions.upload_media_player(token, player_id, link)

                return redirect(url_for('index'), reset='change')
            except Exception as e:
                print(f"Error al subir el archivo a AWS: {e}")

    return redirect(url_for('index', reset='change'))


@app.route('/simulate_api')
def simulate_api():
    #token = obtener_token()
    get_players = ModelActions.getPlayerList(token)
    print(get_players)
    return render_template('simulate-api.html', players_info=get_players)

@app.route('/submit_form_simulate_api', methods=['POST'])
def submit_form_simulate_api():
    #token = '0ce1973ddb9a293cf177e3626135078a'
    #token = obtener_token()
    if request.method == 'POST':
        selected_player_id = request.form.get('playerId')
        temperature_variant = request.form.get('temperature')
        print(f"Selected Player ID: {selected_player_id}")
        print(f"Temperature Variant: {temperature_variant}")
        ModelActions.upload_media_player_simulate(token, selected_player_id, temperature_variant)
    return redirect(url_for('index'))


@app.route('/download_report')
def download_report():
     # Obtener la fecha y hora actual
    now = datetime.datetime.now()
    date = now.strftime("%d/%m/%Y")

    # Formatear la fecha y hora actual según tu especificación
    formatted_date = now.strftime("%d%m%Y%H%M%S") + '-' + str(random.randint(100, 999))
    # Ruta del directorio actual del script
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    # Ruta de la imagen
    ruta_imagen = os.path.join(ruta_script, 'static','img', 'black.jpg')
    print("RUTA Imagen: ", ruta_imagen)
    # Leer la imagen en formato base64
    with open(ruta_imagen, 'rb') as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode('utf-8')


    get_players = ModelActions.getPlayerList(token)
    #print(get_players)
    # Ruta al ejecutable wkhtmltopdf en tu sistema
    ruta_wkhtmltopdf = r'/usr/local/bin/wkhtmltopdf'
    #ruta_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=ruta_wkhtmltopdf)
    try:
        contenido_pdf = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Players PopAtelier</title>
                <style>
                    header {{
                        text-align: center;
                    }}
                    img {{
                        max-width: 500px;
                    }}
                    .info {{
                        text-align: left;
                        font-size: 20px;
                        margin-top: 10px;
                        margin-left: 10px;
                    }}
                    .table-container {{
                        margin-top: 20px;
                        margin-left: 10px;
                        width: 98%;
                    }}
                    .headers-doc{{
                        margin-top: 50px;
                    }}
                    table {{
                        border-collapse: collapse;
                        width: 100%;
                        margin-top: 10px;
                    }}
                    th, td {{
                        border: 1px solid black;
                        padding: 8px;
                        text-align: left;
                        vertical-align: top; /* Alineación vertical */
                        line-height: 1.4; /* Ajuste del espaciado vertical */
                    }}
                    th {{
                        background-color: black;
                        color: white;
                        text-align: center;
                    }}
                    hr {{
                        margin-top: 50px;
                        border: none;
                        border-top: 2px solid black;
                        width: 100%;
                    }}
                </style>
            </head>
            <body>
                <header>
                    <img src="data:image/jpeg;base64,{img_base64}" alt="Logo"> <!-- Imagen incrustada en formato base64 -->
                    <div class="info">
                        <p><strong>POP ATELIER LLC</strong></p>
                        <p><strong>Date: </strong>{date}</p>
                    </div>
                </header>
        """
        # Construir el contenido del PDF usando los datos recibidos
        contenido_pdf += '<h1>Player information</h1>'
       # Crear una tabla HTML con estilo
        contenido_pdf += '<table border="1" style="border-collapse: collapse; width: 100%; text-align: center;">'
        contenido_pdf += '<tr>'
        contenido_pdf += '<th style="padding: 10px;">Name</th>'
        #contenido_pdf += '<th style="padding: 10px;">Player ID</th>'
        contenido_pdf += '<th style="padding: 10px;">Serial Number</th>'
        contenido_pdf += '<th style="padding: 10px;">IP Address</th>'
        contenido_pdf += '<th style="padding: 10px;">Product Name</th>'
        contenido_pdf += '<th style="padding: 10px;">Online Status</th>'
        contenido_pdf += '<th style="padding: 10px;">Last Online Time</th>'
        contenido_pdf += '</tr>'

        for player in get_players:
            # Obtener el estado en línea y establecer el color del cuadrado con bordes redondeados
            status_color = 'green' if player["onlineStatus"] == 1 else 'red'
            
            contenido_pdf += '<tr>'
            contenido_pdf += f'<td style="padding: 10px;">{player["name"]}</td>'
            #contenido_pdf += f'<td style="padding: 10px;">{player["playerId"]}</td>'
            contenido_pdf += f'<td style="padding: 10px;">{player["sn"]}</td>'
            contenido_pdf += f'<td style="padding: 10px;">{player["ip"]}</td>'
            contenido_pdf += f'<td style="padding: 10px;">{player["productName"]}</td>'
            contenido_pdf += f'<td style="padding: 5px; text-align: center; color: white; background-color: {status_color}; border-radius: 0px;">&nbsp;</td>'
            contenido_pdf += f'<td style="padding: 10px;">{player["lastOnlineTime"]}</td>'
            contenido_pdf += '</tr>'

        contenido_pdf += '</table>'

        contenido_pdf += '</body></html>'

        pdfkit_options = {
            'page-size': 'A4',
            'encoding': 'UTF-8',  # Especificar la codificación UTF-8
            # Otras opciones de configuración si las necesitas
        }

        # Generar el PDF
        pdf = pdfkit.from_string(contenido_pdf, False, configuration=config, options=pdfkit_options)

        # Crear la respuesta con el PDF como descarga
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=report-players.pdf'

        return response
    except Exception as e:
        print("Error:", e)  # Imprime el error en la consola del servidor
        return "Error al generar el PDF", 500
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)

@app.route('/')
def index():
    return redirect(url_for('login'))  

@app.route('/home')
@login_required
def home():
    #token = '0ce1973ddb9a293cf177e3626135078a'
    #token = obtener_token()
    get_players = ModelActions.getPlayerList(token)
    get_logs = ModelActions.get_logs(token)
    #print(get_players)
    num_players = len(get_players)
    num_online = sum(player['onlineStatus'] == 1 for player in get_players)
    num_offline = sum(player['onlineStatus'] == 0 for player in get_players)
    reset_status = request.args.get('reset', None)
    send_report_status = request.args.get('sendreport', None)
    return render_template('home.html', players_info=get_players, reset_status=reset_status, send_report_status = send_report_status, num_players=num_players, num_online=num_online, num_offline=num_offline, get_logs=get_logs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    current_user_mode = 0  # Establecer el modo predeterminado en 0 si no se encuentra ningún usuario

    if request.method == 'POST':
        print(request.form['username'])
        print(request.form['password'])
        user = User(0, request.form['username'], request.form['password'], 0, 0)
        logged_user = ModelUser.login(db, user)
        if logged_user:
            current_user_mode = logged_user.mode  # Actualizar el valor de current_user_mode si se encuentra un usuario
            print("MODE: ", current_user_mode)
            print("IDROL: ", logged_user.idRol)
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Invalid Password...")
        else:
            flash("User not found...")
    return render_template('auth/login.html', current_user_mode=current_user_mode)

if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=puerto)
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.run()

