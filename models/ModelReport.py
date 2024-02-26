import datetime
import pdfkit
import requests


class ModelReport:

    def requirementsPDF(self):
        now = datetime.datetime.now()
        date = now.strftime("%d/%m/%Y")
        ruta_wkhtmltopdf = r'C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe'
        # ruta_wkhtmltopdf = r'/usr/local/bin/wkhtmltopdf'
        config = pdfkit.configuration(wkhtmltopdf=ruta_wkhtmltopdf)

        return date, config
    
    @classmethod
    def generateReport(cls, img_base64, get_players):
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
            #contenido_pdf += '<th style="padding: 10px;">IP Address</th>'
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
                #contenido_pdf += f'<td style="padding: 10px;">{player["ip"]}</td>'
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

            return pdf
        except Exception as e:
            print("Error:", e)  # Imprime el error en la consola del servidor
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
        if response.status_code == 200:
            return jsonify({'message': 'Datos enviados correctamente a la API.'}), 200
        else:
            return jsonify({'error': 'Hubo un problema al enviar los datos a la API.'}), 500