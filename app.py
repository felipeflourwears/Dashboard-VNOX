import time
import os
import string
import random
import base64
import json


from flask import Flask, g, render_template, request, redirect, url_for, flash, jsonify, make_response, session, flash

#Instances Models
from models.ModelToken import ModelToken
from models.ModelActions import ModelActions
from models.ModelUser import ModelUser
from models.ModelS3 import ModelS3
from models.ModelReport import ModelReport
from models.ModelVnnox import ModelVnnox
from models.ModelZkong import ModelZkong

from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from config import config
from config import Config, DevelopmentConfig

#Entities
from models.entities.User import User

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



# Configuración de la aplicación
app = Flask(__name__)
# Configuración de la base de datos
app.config.from_object(DevelopmentConfig)
db = MySQL(app)
# Configuración de Flask-WTF CSRF y Flask-Login
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
# Instancias de modelos
model_token = ModelToken() 
model_actions = ModelActions()
model_s3 = ModelS3()
model_vnnox = ModelVnnox()
model_zkong = ModelZkong()

# Imprimir la configuración de la base de datos directamente desde DevelopmentConfig
config_instance = DevelopmentConfig()
#config_instance.print_secret_key()
#config_instance.print_database_config()
load_dotenv()
login_manager_app = LoginManager(app)



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'gif'}

token = '7051bbfe8975803496c428c6be7a2063'

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

#token = obtener_token()
    
@app.route('/reset_player/<string:player_id>', methods=['GET'])
@login_required
def reset_player(player_id):
    try:
        #token = obtener_token()
        print(f"Token: {token}")
        
        ModelActions.reset_player(token, player_id)
        print(f"Player reset successfully: {player_id}")

        # Redirigir al usuario a la ruta principal después de resetear el player
        return redirect(url_for('home', reset='reset'))
    except Exception as e:
        print(f"Error resetting player: {str(e)}")
        # Aquí puedes agregar un manejo más específico del error si es necesario
        return render_template('404.html', error_message=str(e))
    

@app.route('/send_report')
@login_required
def send_report():
    #token = obtener_token()
    try:
        mail = request.args.get('email')
        ModelReport.send_report(mail, token)
        print("Dentro del try")
        return jsonify(success=True, message="Report sent successfully!")
    except Exception as e:
        print(f"Error sending report: {str(e)}")
        return jsonify(success=False, message=str(e))

@app.route('/edit_player/')
@login_required
def edit_player():
    #token = obtener_token()
    # Obtener los parámetros de la URL
    get_logs = ModelActions.get_logs(token)
    player_id = request.args.get('player_id')
    ip = request.args.get('ip')
    name = request.args.get('name')
    
    # Generar una cadena aleatoria para evitar el almacenamiento en caché
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

    
    #token = '0ce1973ddb9a293cf177e3626135078a'
    ModelActions.get_screnn_player(token, player_id)
    
    # Imprimir los valores (puedes eliminar esto en producción)
    print(f"Player ID: {player_id}, IP: {ip}, Name: {name}")
    
    # Renderizar la plantilla con los valores y la cadena aleatoria
    return render_template('edit-player.html', player_id=player_id, ip=ip, name=name, random_string=random_string, get_logs=get_logs)

@app.route('/submit_form_media', methods=['POST'])
@login_required
def submit_form_media():
    player_id = request.form.get('playerId')
    if 'imageUpload' in request.files:
        file = request.files['imageUpload']
        
        if file and allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                print("Filename: ", filename)
                media_type = 'image' if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')) else 'video'
                print("Type: ", media_type)
                
                # Utiliza la función de carga a S3
                model_s3.upload_test(file, media_type, player_id)
                
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
                ModelActions.upload_media_player(token, player_id, link)
            except Exception as e:
                print(f"Error al subir el archivo a AWS: {e}")
    return redirect(url_for('home', reset='change'))
    

@app.route('/media/')
@login_required
def media():
    # Obtener parámetros de búsqueda y página
    query = request.args.get('q', '')  # Obtener parámetro de búsqueda (default '')
    page_number = int(request.args.get('page', 1))  # Obtener parámetro de página (default 1)
    
    # Realizar la búsqueda si hay una consulta
    if query:
        media = model_s3.search_media(query)
    else:
        media = model_s3.list_media()  # Obtener todos los medios
    
    # Calcular el número total de medios
    total_media = len(media)
    
    # Calcular el número total de páginas
    total_pages = (total_media + model_s3.pagination_limit - 1) // model_s3.pagination_limit
    
    # Calcular el rango de páginas a mostrar
    max_pages = 5  # Número máximo de páginas a mostrar en la paginación
    start_range = max(1, page_number - max_pages // 2)
    end_range = min(total_pages, start_range + max_pages - 1)
    start_range = max(1, end_range - max_pages + 1)
    
    # Obtener los medios para la página actual
    start_index = (page_number - 1) * model_s3.pagination_limit
    end_index = min(start_index + model_s3.pagination_limit, total_media)
    media = media[start_index:end_index]

    total_storage = model_s3.get_bucket_size()
    #print("Total Storage: ", total_storage)
    total_videos = model_s3.count_files_by_extension(['.mp4'])
    total_images = model_s3.count_files_by_extension(['.gif', '.jpg', '.jpeg', '.png'])
    # Renderizar la plantilla HTML con los resultados
    return render_template('media.html', objects=media, query=query, page_number=page_number, total_pages=total_pages, start_range=start_range, end_range=end_range, total_storage=total_storage, total_videos=total_videos, total_images=total_images)

@app.route('/upload_media', methods=['POST'])
def upload_media():
    if request.method == 'POST':
        file = request.files['file']  # Obtener el archivo enviado desde el cliente
        tags_received = request.form['tag']
        filename = file.filename  # Obtener el nombre del archivo
        print(type(file))
        print(type(filename))
        print("Archivo recibido:", filename)
        print("Tag recibido:", tags_received)  # Imprimir el tag
        
        unique_filename = model_s3.upload_file_to_s3(file)
        tags = model_s3.adapt_tag(tags_received)
        model_s3.put_tags(unique_filename, tags)
        return redirect('/media')
    
@app.route('/delete', methods=['POST'])
def delete_items():
    selected_items = request.json['selectedItems']
    print("Datos recibidos:", selected_items)
    model_s3.delete_files(selected_items)
    return redirect('/media')
     
def status_404(error):
    return render_template("404.html")

# Manejar el error 401 (Unauthorized)
@app.errorhandler(401)
def unauthorized(error):
    return render_template('401.html'), 401
    
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
    if not current_user.is_authenticated:
        return redirect(url_for('login'))
    user = ModelUser.get_by_id(db, current_user.id)
    return render_template('home.html', user=user)


@app.route('/reports')
@login_required
def reports():
    get_logs = ModelActions.get_logs(token)
    return render_template('reports.html', get_logs=get_logs)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    current_user_mode = 0  # Establecer el modo predeterminado en 0 si no se encuentra ningún usuario

    if request.method == 'POST':

        email = request.form['correo']
        password = request.form['password']
        code = request.form['code']

        print("Email: ", email)
        print("PASSWORD: ", password)
        print("CODE: ", code)
    

        user = User(0, None, email, password, 0, None, None, None, None, None, "")
        
        verify_email = ModelUser.email_exists(db, email)
        print("VERIFY: ",verify_email)

        if verify_email:
            logged_user = ModelUser.login(db, user)
            print(logged_user)

            if logged_user:
                print("ID: ", logged_user.id)
                print("username: ", logged_user.username)
                print("Email: ", logged_user.email)
                print("PASSWORD: ", logged_user.password)
                print("IDROL: ", logged_user.idRol)
                print("Fullname: ", logged_user.fullname)
                print("VNNOX: ", logged_user.vnnox)
                print("ZKONG: ", logged_user.zkong)
                print("MAGICINFO: ", logged_user.magicInfo)
                print("HEXNODE: ", logged_user.hexnode)
                print("idCustomer: ", logged_user.idCustomer)
                session['idCustomer'] = logged_user.idCustomer

            
                # Verifica si el código enviado coincide con el código almacenado en la sesión
                if 'verification_code' in session and session['verification_code'] == code:
                    if logged_user.password:
                        login_user(logged_user)
                        # Limpia el código almacenado en la sesión después de su uso
                        session.pop('verification_code', None)
                        return redirect(url_for('home'))
                    else:
                        flash("Invalid Password...")
                else:
                    flash("Incorrect verification code...")
                    session.pop('verification_code', None)  # Elimina el código almacenado en la sesión
            else:
                flash("User not found...")
                session.pop('verification_code', None)  # Elimina el código almacenado en la sesión
        else:
            flash("Email not found...")
            session.pop('verification_code', None)  # Elimina el código almacenado en la sesión

    return render_template('auth/login.html', current_user_mode=current_user_mode)


@app.route('/send_code', methods=['POST'])
def send_code():
    print("Entre al send code")
    email = request.form.get('email')
    print("EMAIL: ", email)
    verify_email = ModelUser.email_exists(db, email)
    print(verify_email)
    if verify_email:
        code_sent = ModelUser.code_verification(email)
        print(code_sent)
        session['verification_code'] = code_sent
        stored_code = session['verification_code']
        return jsonify({'message': 'Code sent successfully'}), 200
    else:
        return jsonify({'error': 'Email not found'}), 404



@app.route("/vnnox", methods=["GET", "POST"])
def vnnox():
    idCustomer = session.get('idCustomer')
    if idCustomer is None:
        flash("User not logged in or session expired.")
        return redirect(url_for('login'))
    
    # Obtener los datos reales de la API usando model_vnnox.consumir_api
    data = model_vnnox.request_data_api(token, idCustomer)
    print("Data: ", data)  # Asegúrate de que los datos se impriman correctamente para verificar la estructura
    
    # Inicializar variables
    player_ids = []
    players_info = []
    
    # Procesar los datos si existen
    if data:
        players_info = data[0]
        player_ids = [player['playerId'] for player in players_info]

    hello = model_vnnox.get_screen_player(token, player_ids)
    print(hello)
    # Contar jugadores en línea y fuera de línea
    num_online = sum(player['onlineStatus'] == 1 for player in players_info)
    num_offline = sum(player['onlineStatus'] == 0 for player in players_info)
    
    # Número total de jugadores
    num_players = len(players_info)
    #print(num_offline)
    #print(num_online)
    #print(num_players)
    
    return render_template('vnnox.html', players_info=players_info, player_ids=player_ids, num_players=num_players, num_online=num_online, num_offline=num_offline, page="vnnox")

@app.route('/download_report_vnnox', methods=['GET', 'POST'])
@login_required
def download_report_vnnox():
    try:  
        player_ids = request.form.getlist('player_ids[]')
        total_player_ids = len(player_ids)
        print("TOTAL BefoRE: ", total_player_ids)
        # Obtiene los datos de los jugadores usando ModelReport.getPlayerList
        get_players = ModelReport.getPlayerList(token, player_ids)
        total = len(get_players)
        print("TOTAL AFTERR: ", total)

        # Ruta de la imagen
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_imagen = os.path.join(ruta_script, 'static','img', 'black.jpg')

        # Leer la imagen en formato base64
        with open(ruta_imagen, 'rb') as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        

        # Generar el informe en formato PDF
        #pdf_content = ModelReport.generateReport(img_base64, get_players, token)
        pdf_content = ModelReport.generar_pdf(token, get_players)
        if pdf_content:
            # Crear la respuesta con el PDF como descarga
            response = make_response(pdf_content)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename=report-players.pdf'
            return response
        else:
            return render_template('error.html', error='Error al generar el PDF'), 500

    except Exception as e:
        print("Error al generar el PDF:", e)  # Maneja el error apropiadamente
        return render_template('error.html', error=str(e)), 500
    

@app.route('/download_report_zkong')
@login_required
def download_report_zkong():
    try:
        playerIdsCoca = [
            "02f731f425cd4295a914595ee5309af8",
            "23916f448a3e488f9aaaabd6c32a19e8",
            "a00d95f6b2964b5aafc4516a02676e23",
            "fe17a17ee4d451ecc31d5391eeea30de",
            "6eda146077f54c4ea6a8dad94408aaf9",
            "c85072abef3b4676b8c1895795f31a0b",
            "cca07f360ddb4f73bbe82f094dc62bc2",
            "dee2e4d70db248c19579dae1f998f754",
            "b3219585e524412f920d4cab9abc0bde",
            "a42b82d6f9154ee38e0587a34f365590",
            "c64b9c27bc804d2aa71fc8d762d560e3",
            "76f46e96362244eeb7698796b6ade240",
            "4db0f13e2eba4e89b01f9634a1920b1f",
            "dfd889e1c61c4346a9372399d62edd37",
            "23178b68d17b41f4ae91f762f7b2b447",
            "ce8e75bde7124fbc946306186970f368",
            "256ea17ec4da4836896948dd3f15a323",
            "bf9eba224b4f49ddba5768ffd41bef3a",
            "184719cfb545e337c6e5fc8793a96b75",
            "70429d2f73dc4e58b9988036b92c2a98",
            "da9e35672bd1c9fdf583fb5876361932",
            "d40dc00ab57be6f54f8f3288bf961dfd"
        ]
        get_players = ModelReport.getPlayerList(token, playerIdsCoca)
        print(get_players)
       
        # Ruta de la imagen
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_imagen = os.path.join(ruta_script, 'static','img', 'black.jpg')

        # Leer la imagen en formato base64
        with open(ruta_imagen, 'rb') as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
        

        # Generar el informe en formato PDF
        #pdf_content = ModelReport.generateReport(img_base64, get_players, token)
        pdf_content = ModelReport.generar_pdf(token, get_players)

        if pdf_content:
            # Crear la respuesta con el PDF como descarga
            response = make_response(pdf_content)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename=report-players.pdf'
            return response
        else:
            return render_template('error.html', error='Error al generar el PDF'), 500

    except Exception as e:
        print("Error al generar el PDF:", e)  # Maneja el error apropiadamente
        return render_template('error.html', error=str(e)), 500
    
    
@app.route("/zkong", methods=["GET", "POST"])
def zkong():
    idCustomer = session.get('idCustomer')
    if idCustomer is None:
        flash("User not logged in or session expired.")
        return redirect(url_for('login'))
    
    token_zkong = model_zkong.login()
    data = model_zkong.request_data_api(token_zkong, idCustomer)
    
    players_info = data[0] if data else []  # Ajusta según cómo se estructuran realmente tus datos
    
    num_online = sum(player.get('statusOne') == 1 for player in players_info)
    num_offline = sum(player.get('statusOne') == 'NO' for player in players_info)
    num_players = len(players_info)
    
    return render_template('zkong.html', players_info=players_info, num_players=num_players, num_online=num_online, num_offline=num_offline, page="zkong")





if __name__ == '__main__':

    app.config.from_object(config['development'])
    # Imprimir las credenciales de la base de datos
    #print(f"Database Config LF: {app.config['MYSQL_HOST']}, {app.config['MYSQL_USER']}, {app.config['MYSQL_PASSWORD']}, {app.config['MYSQL_DB']}")
    csrf.init_app(app)
    app.register_error_handler(404, status_404)
    app.run()

