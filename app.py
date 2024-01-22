from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort

#Instances Models
from models.ModelToken import ModelToken
from models.ModelActions import ModelActions
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

import time
import os
import string
import random

# Variables globales para almacenar el token y su tiempo de expiración
token_info = {
    'token': None,
    'expiration_time': 0
}

app = Flask(__name__)
model_token = ModelToken() 
model_actions = ModelActions()
load_dotenv()


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4'}

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
        token = obtener_token()
        print(f"Token: {token}")
        
        ModelActions.reset_player(token, player_id)
        print(f"Player reset successfully: {player_id}")

        # Redirigir al usuario a la ruta principal después de resetear el player
        return redirect(url_for('index', reset='change'))
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
    player_id = request.args.get('player_id')
    ip = request.args.get('ip')
    name = request.args.get('name')
    
    # Generar una cadena aleatoria para evitar el almacenamiento en caché
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    token = obtener_token()
    ModelActions.get_screnn_player(token, player_id)
    
    # Imprimir los valores (puedes eliminar esto en producción)
    print(f"Player ID: {player_id}, IP: {ip}, Name: {name}")
    
    # Renderizar la plantilla con los valores y la cadena aleatoria
    return render_template('edit-player.html', player_id=player_id, ip=ip, name=name, random_string=random_string)

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
                
                token = obtener_token()  # Asegúrate de tener definida la función obtener_token()
                ModelActions.upload_media_player(token, player_id, link)

                return redirect(url_for('index'))
            except Exception as e:
                print(f"Error al subir el archivo a AWS: {e}")

    return redirect(url_for('index', sendreport='sendreport'))


@app.route('/simulate_api')
def simulate_api():
    token = obtener_token()
    get_players = ModelActions.getPlayerList(token)
    print(get_players)
    return render_template('simulate-api.html', players_info=get_players)

@app.route('/submit_form_simulate_api', methods=['POST'])
def submit_form_simulate_api():
    token = obtener_token()
    if request.method == 'POST':
        selected_player_id = request.form.get('playerId')
        temperature_variant = request.form.get('temperature')
        print(f"Selected Player ID: {selected_player_id}")
        print(f"Temperature Variant: {temperature_variant}")
        ModelActions.upload_media_player_simulate(token, selected_player_id, temperature_variant)
    return redirect(url_for('index'))


@app.route('/')
def index():
    token = obtener_token()
    get_players = ModelActions.getPlayerList(token)
    print(get_players)
    num_players = len(get_players)
    num_online = sum(player['onlineStatus'] == 1 for player in get_players)
    num_offline = sum(player['onlineStatus'] == 0 for player in get_players)
    reset_status = request.args.get('reset', None)
    send_report_status = request.args.get('sendreport', None)
    return render_template('index.html', players_info=get_players, reset_status=reset_status, send_report_status = send_report_status, num_players=num_players, num_online=num_online, num_offline=num_offline)

if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=puerto)
    app.run()