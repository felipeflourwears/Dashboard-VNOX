import datetime
import pdfkit
import requests
import time
import matplotlib.pyplot as plt
import json


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
    def generar_pdf_vnnox(cls, token, datos_api):
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
                                    <th>No.</th>
                                    <th>Status</th>
                                    <th>Name</th>
                                    <th>Serial Number</th>
                                    <th>Last Online YYYY/MM/DD</th>
                                    <th>Screenshot</th>
                                </tr>
                            </thead>
                            <tbody>
            """
            i = 0
            for fila in datos_api:
                i+=1
                online_status_circle = "circle-green" if fila["onlineStatus"] == 1 else "circle-red"

                contenido_pdf += f"""
                    <tr>
                        <td>{i}</td>
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
            """path_to_save = "static/reports/ReportPopAtelier.pdf"
            with open(path_to_save, "wb") as file:
                file.write(pdf)"""

            return pdf
        except Exception as e:
            print("Error:", e)
            return "Error al generar el PDF", 500

    @classmethod    
    def generar_pdf_zkong(cls, datos_api):
        date, config = cls().requirementsPDF()
        onlinePlayer = 0
        offlinePlayer = 0

        # Reemplazar comillas simples por comillas dobles
        datos_api = datos_api.replace("'", '"')

        # Convertir la cadena JSON a una lista de diccionarios
        try:
            datos_api = json.loads(datos_api)
        except json.JSONDecodeError as e:
            print("Error al decodificar JSON:", e)
            return None
    
        try:
            for fila in datos_api[0]:
                if fila["statusOne"] == 1 and fila["statusTwo"] == 1:
                    onlinePlayer += 1
                else:
                    offlinePlayer += 1

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
                            background-color: #FFFFFF; /* Fondo blanco */
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
                            color: #FFFFFF; /* Texto en blanco */
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
                            background-color: #F2F2F2;
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
                            color: #FFFFFF;
                        }}
                        td:last-child {{
                            width: 100px; /* Ajusta el tamaño según tus necesidades */
                        }}
                        .status-cell {{
                            width: 60px; /* Ajusta el tamaño de la celda de estado */
                            text-align: center; /* Centra el contenido de la celda */
                        }}
                        .tienda-cell {{
                            width: 200px; /* Ajusta el tamaño de la celda de tienda */
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
                                    <th>Store</th>
                                    <th>Screen One</th>
                                    <th>LastOnline</th>
                                    <th>Status</th>
                                    <th>Screen Two</th>
                                    <th>LastOnline</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody>
            """
            for fila in datos_api[0]:
                online_status_circleO = "circle-green" if fila["statusOne"] == 1 else "circle-red"
                online_status_circleT = "circle-green" if fila["statusTwo"] == 1 else "circle-red"
                contenido_pdf += f"""
                    <tr>
                        <td>{fila["tienda"]}</td>
                        <td>{fila["duidOne"]}</td>
                        <td>{fila["lastReportTimeOne"]}</td>
                        <td><div class="circle {online_status_circleO}"></div></td>
                        <td>{fila["duidTwo"]}</td>
                        <td>{fila["lastReportTimeTwo"]}</td>
                        <td><div class="circle {online_status_circleT}"></div></td>
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
            return pdf
        except Exception as e:
            print("Error:", e)
            return None
        
    @classmethod    
    def generar_pdf_hexnode(cls, datos_api):
        date, config = cls().requirementsPDF()
        onlinePlayer = 0
        offlinePlayer = 0
        
        try:
            for fila in datos_api:
                if fila["compliant"] == 0:
                    offlinePlayer += 1
                elif fila["compliant"] == 1:
                    onlinePlayer += 1
            contenido_pdf = f"""
                <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            height: 100vh;
                            margin: 0;
                            background-color: #FFFFFF; /* Fondo blanco */
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
                            color: #FFFFFF; /* Texto en blanco */
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Sombra */
                        }}
                        .card:nth-child(2) {{
                            background-color: #2196F3;
                        }}
                        .card:nth-child(3) {{
                            background-color: #4CAF50;
                        }}
                        .table-container {{
                            display: flex;
                            justify-content: center;
                            width: 100%;
                            padding: 0 20px; /* Ajusta el padding para tener espacio a los lados */
                        }}
                        table {{
                            width: 100%;
                            margin-top: 20px;
                            background-color: #FFFFFF;
                            border: 1px solid #000000;
                            border-collapse: collapse;
                        }}
                        th, td {{
                            border: 1px solid #000000; /* Bordes de celda en negro */
                            text-align: left;
                            padding: 8px;
                        }}
                        th {{
                            background-color: #F2F2F2;
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
                            color: #FFFFFF;
                        }}
                        td:last-child {{
                            width: 100px; /* Ajusta el tamaño según tus necesidades */
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="logo">
                            <img src="https://www.retailmibeex.net/apiVnnox/black.jpg" alt="Logo">
                        </div>
                        <div class="cards">
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
                        </div>
                        <div class="table-container">
                            <table>
                                <thead>
                                    <tr>
                                        <th>Store</th>
                                        <th>Type</th>
                                        <th>Status</th>
                                        <th>LastOnline YYYY/MM/DD</th>
                                    </tr>
                                </thead>
                                <tbody>
                """
            for fila in datos_api:
                online_status_circle = "circle-green" if fila["compliant"] == 1 else "circle-red"
                contenido_pdf += f"""
                    <tr>
                        <td>{fila["tienda"]}</td>
                        <td>{fila["cliente"]}</td>
                        <td><div class="circle {online_status_circle}"></div></td>
                        <td>{fila["last_reported"]}</td>
                    </tr>
                """
            contenido_pdf += """
                                </tbody>
                            </table>
                        </div>
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
            return pdf
        except Exception as e:
            print("Error:", e)
            return None
        
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
