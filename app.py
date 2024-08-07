import time
import os
import string
import random
import base64
import json
import ast
import re



from flask import Flask, g, render_template, request, redirect, url_for, flash, jsonify, make_response, session, flash

#Instances Models
from models.ModelToken import ModelToken
from models.ModelActions import ModelActions
from models.ModelUser import ModelUser
from models.ModelS3 import ModelS3
from models.ModelReport import ModelReport
from models.ModelVnnox import ModelVnnox
from models.ModelZkong import ModelZkong
from models.ModelClaroConnect import ModelClaroConnect
from models.ModelHexnode import ModelHexnode

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
model_claro_connect = ModelClaroConnect()
model_hexnode = ModelHexnode()

# Imprimir la configuración de la base de datos directamente desde DevelopmentConfig
config_instance = DevelopmentConfig()
#config_instance.print_secret_key()
#config_instance.print_database_config()
load_dotenv()
login_manager_app = LoginManager(app)



ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'gif'}


token = '1918db4017b698597f3a5c072ccf5b51'

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
    

        user = User(0, None, email, password, 0, None, None, None, None, None, None, None, "")
        
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
                print("PiSignage: ", logged_user.pisignage)
                print("kosStudio: ", logged_user.kosStudio)
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
    print("--------------------------------------")
    print("Data API JOSSS")
    print(data)
    print(type(data))
    print("--------------------------------------")
    # Inicializar variables
    player_ids = []
    players_info = []
    
    # Procesar los datos si existen
    if data:
        players_info = data[0]
        player_ids = [player['playerId'] for player in players_info]

    get_screen = model_vnnox.get_screen_player(token, player_ids)
    print("Result Get Screen: ", get_screen)
   
    # Contar jugadores en línea y fuera de línea
    num_online = sum(player['onlineStatus'] == 1 for player in players_info)
    num_offline = sum(player['onlineStatus'] == 0 for player in players_info)
    
    # Número total de jugadores
    num_players = len(players_info)
    #print(num_offline)
    #print(num_online)
    #print(num_players)
    
    return render_template('vnnox.html', players_info=players_info, player_ids=player_ids, num_players=num_players, num_online=num_online, num_offline=num_offline, page="vnnox")

@app.route('/view-vnnox/', methods=['POST'])
@login_required
def view_vnnox():
    if request.method == 'POST':
        # Obtener los datos del formulario
        player_id = request.form.get('player_id')
        iccid = request.form.get('iccid')
        imsi = request.form.get('imsi')
        msisdn = request.form.get('msisdn')
        store = request.form.get('store')

        #token_cc = model_claro_connect.authenticate_cc()
        #print("Token: ", token)
        #inSession, sessionStartTime, data = model_claro_connect.claroConnectApi(imsi, token_cc)
        #print(data)

        # Por ejemplo, generar una cadena aleatoria para evitar el almacenamiento en caché
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        inSession = False
        sessionStartTime = "No date"

        # Renderizar la plantilla con los valores y la cadena aleatoria
        return render_template('view-vnnox.html', 
                               player_id=player_id, 
                               imsi=imsi, 
                               iccid=iccid, 
                               msisdn=msisdn, 
                               store=store, 
                               random_string=random_string,
                               inSession = inSession, 
                               sessionStartTime = sessionStartTime)
    else:
        # Manejar otro comportamiento si no es POST (opcional)
        return 'Método no permitido', 405  # Código de error 405 para método no permitido

@app.route('/download_report_vnnox', methods=['POST'])
@login_required  # Asegúrate de tener esta función decoradora implementada
def download_report_vnnox():
    try:
        idCustomer = session.get('idCustomer')
        if idCustomer is None:
            flash("User not logged in or session expired.")
            return redirect(url_for('login'))
        # Obtener los datos reales de la API usando model_vnnox.consumir_api
        data = model_vnnox.request_data_api(token, idCustomer)
        # Generar el informe en formato PDF
        #pdf_content = ModelReport.generateReport(img_base64, get_players, token)
        pdf_content = ModelReport.generar_pdf_vnnox(token, data)
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
    data_pdf = data
    
    num_online = sum(player.get('statusOne') == 1 for player in players_info)
    num_offline = sum(player.get('statusOne') == 0 for player in players_info)
    num_players = len(players_info)
    
    return render_template('zkong.html', players_info=players_info, datos_pdf = data_pdf, num_players=num_players, num_online=num_online, num_offline=num_offline, page="zkong")

@app.route('/view-zkong/', methods=['POST'])
@login_required
def view_zkong():
    csrf_token = request.form.get('csrf_token')
    player_duidOne = request.form.get('player_duidOne')
    player_statusOne = request.form.get('player_statusOne')
    player_duidTwo = request.form.get('player_duidTwo')
    player_statusTwo = request.form.get('player_statusTwo')
    iccid = request.form.get('iccid')
    imsi = request.form.get('imsi')
    msisdn = request.form.get('msisdn')
    store = request.form.get('store')
    lastReportTimeOne = request.form.get("lastReportTimeOne")
    lastReportTimeTwo = request.form.get("lastReportTimeTwo")
    
    """ token_cc = model_claro_connect.authenticate_cc()
    inSession, sessionStartTime, data = model_claro_connect.claroConnectApi(imsi, token_cc)
    print(data) """
    inSession = False
    sessionStartTime = "No date"

    return render_template('view-zkong.html', player_duidOne=player_duidOne, 
                           player_statusOne=player_statusOne, 
                           player_duidTwo=player_duidTwo, 
                           player_statusTwo=player_statusTwo, 
                           imsi=imsi, 
                           iccid=iccid, 
                           msisdn=msisdn, 
                           store=store,
                           lastReportTimeOne=lastReportTimeOne,
                           lastReportTimeTwo=lastReportTimeTwo,
                           inSession = inSession,
                           sessionStartTime = sessionStartTime
                           )

@app.route('/download_report_zkong', methods=['GET', 'POST'])
@login_required
def download_report_zkong():
    try:   
        # Obtener el dato del formulario
        player_ids = request.form.get('player_ids[]')
      
        pdf_content = ModelReport.generar_pdf_zkong(player_ids)
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
    
@app.route("/hexnode", methods=["GET", "POST"])
def hexnode():
    idCustomer = session.get('idCustomer')
    if idCustomer is None:
        flash("User not logged in or session expired.")
        return redirect(url_for('login'))

    data, num_players, num_online, num_offline = model_hexnode.get_devices_summary(idCustomer)
    num_online = 6
    num_offline = 0
    
    return render_template('hexnode.html', players_info = data, num_players=num_players, num_online=num_online, num_offline=num_offline, page="hexnode")

@app.route('/view-hexnode/', methods=['POST'])
@login_required
def view_hexnode():
    if request.method == 'POST':
        # Obtener los datos del formulario
        iccid = request.form.get('iccid')
        imsi = request.form.get('imsi')
        msisdn = request.form.get('msisdn')
        store = request.form.get('store')
        cliente = request.form.get('cliente')

        #token_cc = model_claro_connect.authenticate_cc()
        #inSession, sessionStartTime, data = model_claro_connect.claroConnectApi(imsi, token_cc)

        inSession = True
        sessionStartTime = "No date"

        # Por ejemplo, generar una cadena aleatoria para evitar el almacenamiento en caché
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))


        # Renderizar la plantilla con los valores y la cadena aleatoria
        return render_template('view-hexnode.html',
                               imsi=imsi, 
                               iccid=iccid, 
                               msisdn=msisdn, 
                               store=store,
                               cliente = cliente,
                               random_string=random_string,
                               inSession = inSession, 
                               sessionStartTime = sessionStartTime)
    
@app.route('/download_report_hexnode', methods=['GET', 'POST'])
@login_required
def download_report_hexnode():
    try:
        player_ids_str = request.form.get('players_info[]')

        # Usar ast.literal_eval para evaluar el string como una estructura de datos de Python
        player_ids = ast.literal_eval(player_ids_str)


        # Generar el informe en formato PDF
        #pdf_content = ModelReport.generateReport(img_base64, get_players, token)
        pdf_content = ModelReport.generar_pdf_hexnode(player_ids)
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

if __name__ == '__main__':
    app.config.from_object(config['development'])
    # Imprimir las credenciales de la base de datos
    #print(f"Database Config LF: {app.config['MYSQL_HOST']}, {app.config['MYSQL_USER']}, {app.config['MYSQL_PASSWORD']}, {app.config['MYSQL_DB']}")
    csrf.init_app(app)
    app.register_error_handler(404, status_404)
    app.run()

