import time
import os
import string
import random
import base64


from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response, session

#Instances Models
from models.ModelToken import ModelToken
from models.ModelActions import ModelActions
from models.ModelUser import ModelUser
from models.ModelS3 import ModelS3
from models.ModelReport import ModelReport


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

# Imprimir la configuración de la base de datos directamente desde DevelopmentConfig
config_instance = DevelopmentConfig()
#config_instance.print_secret_key()
#config_instance.print_database_config()
load_dotenv()
login_manager_app = LoginManager(app)



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'gif'}

token = '656cce7a6c44cca33962afd0b4478d98'

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


@app.route('/download_report')
@login_required
def download_report():
    try:
        # Obtener los jugadores
        #get_players = ModelActions.getPlayerList(token)
        get_players2 = ModelActions.getPlayerList_Selected(token)
       
        # Ruta de la imagen
        ruta_script = os.path.dirname(os.path.abspath(__file__))
        ruta_imagen = os.path.join(ruta_script, 'static','img', 'black.jpg')

        # Leer la imagen en formato base64
        with open(ruta_imagen, 'rb') as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

        # Generar el informe en formato PDF
        pdf_content = ModelReport.generateReport(img_base64, get_players2, token)

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
    #token = obtener_token()
    #get_players = ModelActions.getPlayerList(token)
    get_players = model_actions.getPlayerList_Selected(token)
    get_logs = ModelActions.get_logs(token)
    #print(get_players)

    #hello = ModelUser.codeVerification()
    #print(hello)


    num_players = len(get_players)
    num_online = sum(player['onlineStatus'] == 1 for player in get_players)
    num_offline = sum(player['onlineStatus'] == 0 for player in get_players)
    reset_status = request.args.get('reset', None)
    send_report_status = request.args.get('sendreport', None)
    return render_template('home.html', players_info=get_players, reset_status=reset_status, send_report_status = send_report_status, num_players=num_players, num_online=num_online, num_offline=num_offline, get_logs=get_logs)


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

        user = User(0, None, email, password, 0, None)
        
        verify_email = ModelUser.email_exists(db, email)
        print("VERIFY: ",verify_email)

        if verify_email:
            logged_user = ModelUser.login(db, user)

            if logged_user:
                print("ID: ", logged_user.id)
                print("username: ", logged_user.username)
                print("Email: ", logged_user.email)
                print("PASSWORD: ", logged_user.password)
                print("IDROL: ", logged_user.idRol)
                print("Fullname: ", logged_user.fullname)
            
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



@app.route('/test', methods=['POST'])
def test_route():
    if request.method == 'POST':
        data = request.get_json()
        text = data.get('text', '')  # Obtener el texto enviado desde el cliente
        print("Texto recibido:", text)
        return text  # Devolver el texto recibido como respuesta

if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=puerto)
    app.config.from_object(config['development'])
    # Imprimir las credenciales de la base de datos
    #print(f"Database Config LF: {app.config['MYSQL_HOST']}, {app.config['MYSQL_USER']}, {app.config['MYSQL_PASSWORD']}, {app.config['MYSQL_DB']}")
    csrf.init_app(app)
    app.register_error_handler(404, status_404)
    app.run()

