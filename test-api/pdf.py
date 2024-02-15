import pdfkit

def generar_pdf():

    # Ruta al ejecutable wkhtmltopdf en tu sistema
    ruta_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
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
                        <div class="info">
                            <p><strong>POP ATELIER LLC</strong></p>
                            <p><strong>Date: </strong>11-17-2020</p>
                        </div>
                    </header>
            """
        # Construir el contenido del PDF usando los datos recibidos
        contenido_pdf += '<h1>Información</h1>'
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
       
        pdfkit_options = {
            'page-size': 'A4',
            'encoding': 'UTF-8',  # Especificar la codificación UTF-8
            # Otras opciones de configuración si las necesitas
        }

        # Generar el PDF
        pdf = pdfkit.from_string(contenido_pdf, False, configuration=config, options=pdfkit_options)

        # Guardar el PDF en un archivo
        with open('mi_pdf.pdf', 'wb') as file:
            file.write(pdf)

        return "PDF generado correctamente"
    except Exception as e:
        print("Error:", e)  # Imprime el error en la consola del servidor
        return "Error al generar el PDF"


print(generar_pdf())