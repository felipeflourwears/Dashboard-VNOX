import datetime
import pdfkit
import requests

from .ModelConfig import ModelConfig


class ModelReport:

    def requirementsPDF(self):
        now = datetime.datetime.now()
        date = now.strftime("%d/%m/%Y")
        #ruta_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
        ruta_wkhtmltopdf = r'/usr/local/bin/wkhtmltopdf'
        config = pdfkit.configuration(wkhtmltopdf=ruta_wkhtmltopdf)

        return date, config
    
    @classmethod
    def getPlayerList(cls, token, playerIds):
        result_array = []
        api_host = "openapi-us.vnnox.com"
        username = "popatelier"
        endpoint = "/v1/player/get/syncCurrentInfo"
        
        new_url = f"https://{api_host}{endpoint}"
        headers = {
            "username": username,
            "token": token
        }

        try:
            response = requests.post(new_url, headers=headers, json={"playerIds": playerIds})
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

            data = response.json()
            if "status" in data and data["status"] == 0 and "data" in data:
                rows = data["data"]
                result_array.extend([
                    {
                        "playerId": row["playerId"],
                        "name": row["name"],
                        "sn": row["sn"],
                        "lastOnlineTime": row["lastOnlineTime"],
                        "onlineStatus": row["onlineStatus"]
                    }
                    for row in rows
                ])
            else:
                print("La estructura de la respuesta no es la esperada.")

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")

        except Exception as e:
            print(f"Error desconocido: {e}")

        return result_array

    @classmethod      
    def get_screen_player(self, token, player_id):
        api_host = 'openapi-us.vnnox.com'
        new_api_endpoint = '/v1/player/control/screenshot'
        received = 'https://retailmibeex.net/apiVnnox/recibe.php'

        username = ModelConfig.username_auth()
            
        new_url = f"https://{api_host}{new_api_endpoint}"
        print("URL:", new_url)
        headers = {
            'username': username,
            'token': token,
            'Content-Type': 'application/json'  # Asegúrate de incluir el tipo de contenido JSON en los headers
        }

        # Parámetros a enviar en el cuerpo de la solicitud
        request_parameters = {
            "playerIds": [player_id],
            "noticeUrl": received
        }

        # Realizar la nueva solicitud con método POST
        new_response = requests.post(new_url, headers=headers, json=request_parameters)

    
    @classmethod
    def generateReport(cls, img_base64, get_players, token):
        try:
            date, config = cls().requirementsPDF()
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
            contenido_pdf += '<th style="padding: 10px;">Image</th>'
            #contenido_pdf += '<th style="padding: 10px;">IP Address</th>'
            #contenido_pdf += '<th style="padding: 10px;">Product Name</th>'
            contenido_pdf += '<th style="padding: 10px;">Online Status</th>'
            contenido_pdf += '<th style="padding: 10px;">Last Online Time</th>'
            contenido_pdf += '</tr>'
            
            for player in get_players:
                cls.get_screen_player(token, player["playerId"])
                # Obtener el estado en línea y establecer el color del cuadrado con bordes redondeados
                status_color = 'green' if player["onlineStatus"] == 1 else 'red'
                
                contenido_pdf += '<tr>'
                contenido_pdf += f'<td style="padding: 10px;">{player["name"]}</td>'
                #contenido_pdf += f'<td style="padding: 10px;">{player["playerId"]}</td>'
                contenido_pdf += f'<td style="padding: 10px;">{player["sn"]}</td>'
                contenido_pdf += f'<td style="padding: 10px;"><img src="https://retailmibeex.net/apiVnnox/screenPlayers/{player["playerId"]}.jpg" alt="Screenshot" style="max-width: 100px;"></td>'
                #contenido_pdf += f'<td style="padding: 10px;">{player["ip"]}</td>'
                #contenido_pdf += f'<td style="padding: 10px;">{player["productName"]}</td>'
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

            return pdf
        except Exception as e:
            print("Error:", e)  # Imprime el error en la consola del servidor
            return "Error al generar el PDF", 500
        
    @classmethod
    def generar_pdf(cls, token, datos_api):
        print("Entre LFFFFFFFFFFFFFFFFF")
        onlinePlayer = 0
        offlinePlayer = 0
        date, config = cls().requirementsPDF()

        try:
            for fila in datos_api:
                if fila["onlineStatus"] == 0:
                    offlinePlayer = offlinePlayer + 1
                elif fila["onlineStatus"] == 1:
                    onlinePlayer = onlinePlayer + 1

            contenido_pdf = f"""
                <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            display: flex;
                            align-items: center;
                            height: 100vh;
                            margin: 0;
                            background-color: #ffffff; /* Fondo blanco */
                        }}
                        .container {{
                            width: 100%;
                            text-align: center; /* Centrar horizontalmente */
                        }}

                        .logo {{
                            margin-bottom: 20px; /* Espaciado entre el logotipo y las tarjetas */
                        }}

                        .card {{
                            border: none;
                            border-radius: 10px;
                            padding: 20px;
                            text-align: center;
                            width: 200px;
                            display: inline-block;
                            margin-right: 20px; /* Agregado para separar las tarjetas */
                            background-color: #EF5350;
                            color: #ffffff; /* Texto en blanco */
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Sombra */
                        }}
                        .card:nth-child(2) {{
                            background-color: #2196F3; 
                            
                        }}
                        .card:nth-child(3) {{
                            background-color: #4CAF50; 
                        }}
                        table {{
                            width: calc(100% - 40px); /* Ajusta el ancho de la tabla restando el margen derecho de la suma total */
                            margin-top: 20px;
                            background-color: #FFFFFF;
                            border: 1px solid #000000;
                            border-collapse: collapse;
                            margin-right: 20px;
                        }}

                        th, td {{
                            border: 1px solid #000000; /* Bordes de celda en negro */
                            text-align: left;
                            padding: 8px;
                        }}

                        th {{
                            background-color: #f2f2f2;
                            border-bottom: 2px solid #000000; /* Bordes adicionales para las celdas de encabezado */
                        }}

                        .circle {{
                            width: 20px; /* Ajusta el tamaño del círculo */
                            height: 20px; /* Ajusta el tamaño del círculo */
                            border-radius: 50%;
                            display: inline-block;
                            vertical-align: middle;
                        }}

                        .circle-green {{
                            background-color: #4CAF50;
                        }}

                        .circle-red {{
                            background-color: #EF5350;
                        }}

                        th {{
                            background-color: #2196F3;
                            text-align: center;
                            color: #ffffff;
                        }}
                        td:last-child {{
                            width: 300px; /* Puedes ajustar el valor según tus necesidades */
                        }}

                        /* Ajuste del tamaño de la imagen dentro de la última columna */
                        td:last-child img {{
                            width: 100%; /* Ajustar la imagen al 100% del ancho de la columna */
                            height: auto; /* Mantener la proporción original de la imagen */
                            display: table-cell;
                            margin: 0 auto;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="logo">
                            <img src="https://www.retailmibeex.net/apiVnnox/black.jpg" alt="Logo">
                        </div>
                        <div class="card">
                            <h2>Total Players</h2>
                            <p>{onlinePlayer + offlinePlayer}</p>
                        </div>

                        <div class="card">
                            <h2>Online</h2>
                            <p>{onlinePlayer}</p>
                        </div>

                        <div class="card">
                            <h2>Offline</h2>
                            <p>{offlinePlayer}</p>
                        </div>

                        <table>
                            <thead>
                                <tr>
                                    <th>Status</th>
                                    <th>Name</th>
                                    <th>Serial Number</th>
                                    <th>LastOnline YYYY/MM/DD</th>
                                    <th>Screenshot</th>
                                </tr>
                            </thead>
                            <tbody>
            """

            for fila in datos_api:
                cls.get_screen_player(token, fila["playerId"])
                online_status_circle = "circle-green" if fila["onlineStatus"] == 1 else "circle-red"

                contenido_pdf += f"""
                    <tr>
                        <td><div class="circle {online_status_circle}"></div></td>
                        <td>{fila["name"]}</td>
                        <td>{fila["sn"]}</td>
                        <td>{fila["lastOnlineTime"]}</td>
                        <td><img src="https://retailmibeex.net/apiVnnox/screenPlayers/{fila["playerId"]}.jpg" alt="Screenshot"></td>
                    </tr>
                """

            contenido_pdf += """
                            </tbody>
                        </table>
                    </div>
                </body>
                </html>
            """

            pdfkit_options = {
                "page-size": "A4",
                "encoding": "UTF-8",
                # Otras opciones de configuración si las necesitas
            }

            pdf = pdfkit.from_string(contenido_pdf, False, configuration=config, options=pdfkit_options)
            path_to_save = "static/reports/ReportPopAtelier.pdf"
            with open(path_to_save, "wb") as file:
                file.write(pdf)

            return pdf
        except Exception as e:
            print("Error:", e)
            return "Error al generar el PDF", 500
        
    @classmethod
    def send_report(cls,token):        
       # Recupera los datos del formulario
        dato = requests.form['dato']

        # Aquí reemplaza 'tu_token' con el token real que necesitas enviar a la API
        # token = '7f74f6b22572485903aa5c13ec87f085'

        # URL de la API a la que enviar los datos
        url_api = f'https://retailmibeex.net/apiVnnox/postEmail.php?token={token}'

        # Cuerpo de la solicitud que se enviará a la API
        data = {
            'emails': dato
        }

        # Encabezados de la solicitud que incluyen el token de autorización
        headers = {
            'Content-Type': 'application/json',
        }

        # Enviar la solicitud POST a la API con los datos y encabezados
        response = requests.post(url_api, json=data)

        # Verificar si la solicitud fue exitosa
        """if response.status_code == 200:
            return jsonify({'message': 'Datos enviados correctamente a la API.'}), 200
        else:
            return jsonify({'error': 'Hubo un problema al enviar los datos a la API.'}), 500 """