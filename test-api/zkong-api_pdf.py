import pdfkit
import requests
def consumir_api(token, idCustomer):
    url = 'https://retailmibeex.net/apiVnnox/zkongService.php?token='
    url += token
    print(token, url)
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "idCustomer": idCustomer,
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Verificar si hubo errores en la respuesta
        # Decodificar la respuesta JSON
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f'Error al realizar la solicitud: {e}')
        return None

def generar_pdf(datos_api):
        ruta_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=ruta_wkhtmltopdf)
        onlinePlayer = 0
        offlinePlayer = 0
        try:
            for fila in datos_api[0]:
                if fila["statusOne"] == 1 and fila["statusTwo"] == 1:
                    onlinePlayer = onlinePlayer + 1
                else:
                    offlinePlayer = offlinePlayer + 1
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
                            width: 300px; /* Puedes ajustar el valor según tus necesidades */
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
                                    <th>Tienda</th>
                                    <th>DuidOne</th>
                                    <th>LastOnline</th>
                                    <th>Status</th>
                                    <th>DuidTwo</th>
                                    <th>LastOnline>
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
            with open("reporteConFotoB.pdf", "wb") as file:
                file.write(pdf)
            return "PDF generado correctamente"
        except Exception as e:
            print("Error:", e)
            return "Error al generar el PDF"
token = 'eyJhbGciOiJIUzI1NiJ9.eyJyYW5kb20iOiIzMTY0ODU0IiwiaWQiOjI4MTIsImV4cCI6MTcyMDQ1Njc2MiwidGltZXN0YW1wIjoxNzIwNDUzMTYyODUzfQ.-mEriGdO19oL0jONC9ZXeQ03zLtKkyyvfRSFsBPKeRk'
idCustomer = 5
datos_api = consumir_api(token, idCustomer)
print("DATOS: ----------->")
print(datos_api)
print("DATOS: ----------->")
datos_api = [[{'duidOne': 'A0BF4F141D0C', 'duidTwo': '193212CF590C', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Vasco de Quiroga 3800, Lomas de Santa Fe, Contadero, 01210 Ciudad de M?xico, CDMX / Centro Comercial Santa Fe', 'iccid': '895202052349351803', 'imsi': '334020110490348', 'msisdn': '525620026356', 'lastReportTimeOne': '2024-07-01 20:12:30', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-01 20:09:13', 'statusTwo': 0}, {'duidOne': 'D121AE37FED0', 'duidTwo': '3C489AC6E6D0', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Paseo Colon No. 200, 50120 TOLUCA DE LERDO, ESTADO DE MEXICO?', 'iccid': '895202052349351802', 'imsi': '334020110490344', 'msisdn': '525620026355', 'lastReportTimeOne': '2024-07-05 17:14:53', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-05 17:14:58', 'statusTwo': 0}, {'duidOne': 'C87F23176AD0', 'duidTwo': 'C1B261986CD0', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Pase de las Palmas No. 781  Lomas de Chapultepec Miguel Hidalgo Ciudad de M?xico CP. 11560', 'iccid': '895202052349351798', 'imsi': '334020110490338', 'msisdn': '525620026377', 'lastReportTimeOne': '2024-05-16 20:10:24', 'statusOne': 0, 'lastReportTimeTwo': '2024-05-16 20:10:05', 'statusTwo': 0}, {'duidOne': '798787A575D2 ', 'duidTwo': '4DB37071AAD2', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Anillo Perif?rico 4690, Ampliaci?n Jard?nes del Pedregal, 04600 Mexico City - Centro Comercial Perisur', 'iccid': 'Sim ofi S/regis', 'imsi': '', 'msisdn': '', 'lastReportTimeOne': 'NO', 'statusOne': 0, 'lastReportTimeTwo': '2024-06-20 11:29:28', 'statusTwo': 0}, {'duidOne': '1C897579ADD3', 'duidTwo': '12BBB799E9D3', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Blvrd. Interlomas Mz 111, San Fernando\tNaucalpan de Ju?rez CP 52784', 'iccid': '895202052349351801', 'imsi': '334020110490342', 'msisdn': '525620026353', 'lastReportTimeOne': '2024-05-18 11:04:34', 'statusOne': 0, 'lastReportTimeTwo': '2024-05-18 11:04:33', 'statusTwo': 0}, {'duidOne': '91085F5F34D0', 'duidTwo': 'EB92B6264ED0', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Av. Universidad No. 1000 Santa Cruz Atoyac Benito Ju?rez CP 3300', 'iccid': '895202052349351797', 'imsi': '334020110490334', 'msisdn': '525620026376', 'lastReportTimeOne': '2024-07-09 09:29:53', 'statusOne': 1, 'lastReportTimeTwo': '2024-07-09 09:30:29', 'statusTwo': 1}, {'duidOne': '259D3AA756D0', 'duidTwo': 'D7FBA9A022D0', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Avenida Real San Agustin No. 222 Zona San Agust?n, C.P. 66278 NUEVO LEON', 'iccid': '895202052349351804', 'imsi': '334020110490351', 'msisdn': '525620026357', 'lastReportTimeOne': '2024-07-09 09:35:28', 'statusOne': 1, 'lastReportTimeTwo': '2024-07-09 09:35:59', 'statusTwo': 1}, {'duidOne': 'DE40C67DC728', 'duidTwo': 'D76E568C4128', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Hegel No. 345, Lomas de Chapultepec. Miguel Hidalgo CP 11570', 'iccid': '895202052349351810', 'imsi': '334020110490359', 'msisdn': '525620026349', 'lastReportTimeOne': '2024-07-07 01:56:19', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-07 01:54:43', 'statusTwo': 0}, {'duidOne': '6B71357290D0', 'duidTwo': '2395160741D0', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Parroquia No. 179 del Valle Benito Ju?rez CP 3100 CC Galerias Insurgentes', 'iccid': '895202052349351970', 'imsi': '334020110490677', 'msisdn': '525620026365', 'lastReportTimeOne': '2024-06-07 17:49:25', 'statusOne': 0, 'lastReportTimeTwo': '2024-06-07 17:49:28', 'statusTwo': 0}, {'duidOne': '5F1721BA8ED0', 'duidTwo': '7F42972831D0', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Av. Barranca del Muerto No. 479 Col. Merced G?mez, ?lvaro Obreg?n CDMX CP 1600', 'iccid': '895202052349351806', 'imsi': '334020110490354', 'msisdn': '525620026348', 'lastReportTimeOne': '2024-05-20 20:43:46', 'statusOne': 0, 'lastReportTimeTwo': '2024-05-20 20:43:42', 'statusTwo': 0}, {'duidOne': 'C917CB8369E4', 'duidTwo': '8081F885A7E4', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Calzada Acoxpa No.728 Col. Villa Coapa, Tlalpan CDMX CP 14390', 'iccid': '895202052349351800', 'imsi': '334020110490341', 'msisdn': '525620026375', 'lastReportTimeOne': '2024-07-09 09:33:38', 'statusOne': 1, 'lastReportTimeTwo': '2024-07-09 09:32:08', 'statusTwo': 1}, {'duidOne': 'D68F0CE483D0', 'duidTwo': 'AF23A3040ED0', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Blvd. Toluca Metepec No. 126 Col. Coaxustenco, Metepec ESTADO DE M?XICO CP 52140', 'iccid': '895202052349351972', 'imsi': '334020110490679', 'msisdn': '525620026371', 'lastReportTimeOne': '2024-07-09 09:39:11', 'statusOne': 1, 'lastReportTimeTwo': '2024-07-09 09:38:41', 'statusTwo': 1}, {'duidOne': 'BA47B08EA8D0', 'duidTwo': '8ED1DD2A27D0', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'San Luis Potos? No. 214 - 101 Col. Roma Norte, Cuauht?moc CDMX CP 6700', 'iccid': '895202052349351965', 'imsi': '334020110490660', 'msisdn': '525620026359', 'lastReportTimeOne': '2024-07-09 09:32:59', 'statusOne': 1, 'lastReportTimeTwo': '2024-07-09 09:32:29', 'statusTwo': 1}, {'duidOne': 'ED59C193D2D3', 'duidTwo': '8E7DE97EE4D3', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Calzada del Hueso 519 Residencial Miramontes, Tlalpan CP 14300', 'iccid': '895202052349351975', 'imsi': '334020110490683', 'msisdn': '525620026370', 'lastReportTimeOne': '2024-05-03 16:43:10', 'statusOne': 0, 'lastReportTimeTwo': '2024-05-03 16:43:18', 'statusTwo': 0}, {'duidOne': '9A797FE207D0', 'duidTwo': 'AEB4EA4000D0', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Blvd. del Ni?o Poblano 2510, Reserva Territorial Atlixc?yot, 72430 Puebla, Puebla', 'iccid': '895202052349337017', 'imsi': '334020110465964', 'msisdn': '525544782400', 'lastReportTimeOne': '2024-07-09 09:32:21', 'statusOne': 1, 'lastReportTimeTwo': '2024-07-09 09:32:41', 'statusTwo': 1}, {'duidOne': '49441FD1F2D0', 'duidTwo': '979F4CB09CD0', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Prol. Bosques Reforma No. 1813  Bosques de Vista Hermosa Cuajimalpa de Morelos Ciudad de M?xico CP. 05120', 'iccid': '895202052349351969', 'imsi': '334020110490674', 'msisdn': '525620026368', 'lastReportTimeOne': '2024-07-09 09:32:29', 'statusOne': 1, 'lastReportTimeTwo': '2024-07-09 09:31:17', 'statusTwo': 1}, {'duidOne': '6172183644D0', 'duidTwo': '2BC4715A7ED0', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Av. Francisco I. Madero No. 4 Centro Cuauht?moc Ciudad de M?xico CP. 06500', 'iccid': 'Falta ponerle SIM', 'imsi': '', 'msisdn': '', 'lastReportTimeOne': '2024-07-09 09:32:39', 'statusOne': 1, 'lastReportTimeTwo': '2024-07-09 09:32:33', 'statusTwo': 1}, {'duidOne': '9606CDB87528', 'duidTwo': 'ED0A2E0EAE28', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Cto Centro Comercial 2256 Cd. Sat?lite,\tNaucalpan de Ju?rez CP 53100', 'iccid': '895202052349351961', 'imsi': '334020110490650', 'msisdn': '525620026358', 'lastReportTimeOne': '2024-07-09 09:35:54', 'statusOne': 1, 'lastReportTimeTwo': '2024-07-09 09:31:43', 'statusTwo': 1}, {'duidOne': '174731BD8328', 'duidTwo': '82724D3D3B28', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Avenida Rafael Sanzio 150-C Camichines Vallarta, C.P. 45020 JALISCO', 'iccid': '895202052349337019', 'imsi': '334020110465966', 'msisdn': '525544666014', 'lastReportTimeOne': '2024-07-07 20:41:45', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-07 20:44:07', 'statusTwo': 0}, {'duidOne': 'F14B6C80AED0', 'duidTwo': '9EA3266D3AD0', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Av. Central, Fraccionamiento Las Am?ricas S/N Col. Las Am?ricas, Ecatepec de Morelos ESTADO DE M?XICO CP 55076', 'iccid': '895202052349351805', 'imsi': '334020110490353', 'msisdn': '525620026354', 'lastReportTimeOne': '2024-07-09 09:38:48', 'statusOne': 1, 'lastReportTimeTwo': '2024-07-09 09:29:53', 'statusTwo': 1}, {'duidOne': '5CF99E099FD0', 'duidTwo': 'C744778EF5D0', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Av. Cuauht?moc 462 Piedad Narvarte Benito Ju?rez CP 3600', 'iccid': '895202052349351966', 'imsi': '334020110490663', 'msisdn': '525620026364', 'lastReportTimeOne': '2024-07-02 21:54:43', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-02 21:51:29', 'statusTwo': 0}, {'duidOne': '2CC70051FFD0', 'duidTwo': 'F6DABC6BC9D0', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Av. Patriotismo No. 229  San Pedro de los Pinos Benito Ju?rez Ciudad de M?xico CP. 03800', 'iccid': '895202052349351963', 'imsi': '334020110490655', 'msisdn': '525620026361', 'lastReportTimeOne': '2024-06-21 08:27:44', 'statusOne': 0, 'lastReportTimeTwo': '2024-06-21 08:27:44', 'statusTwo': 0}, {'duidOne': '2A8EB80574D0', 'duidTwo': 'DCFC01BBFDD0', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Calle Colector 13 No. 280 Local SA03  Magdalena de las Salinas Gustavo A. Madero Ciudad de M?xico CP. 07760', 'iccid': '895202052349351799', 'imsi': '334020110490339', 'msisdn': '525620026378', 'lastReportTimeOne': '2024-07-09 09:31:30', 'statusOne': 1, 'lastReportTimeTwo': '2024-07-09 09:31:55', 'statusTwo': 1}, {'duidOne': '7E312A87F1D0', 'duidTwo': 'DB9185EC47D0', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Calle 7 No. 451 MZ. 591 Local 31 Altabrisa, C.P. 97130 YUCATAN', 'iccid': 'No hay foto SIM', 'imsi': '', 'msisdn': '', 'lastReportTimeOne': '2024-06-05 14:53:17', 'statusOne': 0, 'lastReportTimeTwo': '2024-06-05 14:51:00', 'statusTwo': 0}, {'duidOne': 'DC6FF0487A28', 'duidTwo': '99DA7C82A628', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Reforma No. 222 Subancla 03Ju?rez Cuauht?moc CP 6600', 'iccid': '895202052349351808', 'imsi': '334020110490356', 'msisdn': '525620026351', 'lastReportTimeOne': '2024-07-03 10:45:33', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-03 10:46:11', 'statusTwo': 0}, {'duidOne': '0AC72B0FA6D0', 'duidTwo': 'E2439030BBD0', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Lago Zurich No. 245  Granada Ampliaci?n Miguel Hidalgo Ciudad de M?xico CP. 11529', 'iccid': '895202052349351809', 'imsi': '334020110490358', 'msisdn': '525620026352', 'lastReportTimeOne': '2024-06-17 20:13:58', 'statusOne': 0, 'lastReportTimeTwo': '2024-06-17 20:09:41', 'statusTwo': 0}, {'duidOne': '5E275E40A9D0', 'duidTwo': 'E325D3DC04D0', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Av. Sor Juana Ines No. 280  San Lorenzo Tlalnepantla Estado de M?xico CP. 54030', 'iccid': '895202052349351807', 'imsi': '334020110490355', 'msisdn': '525620026350', 'lastReportTimeOne': '2024-07-08 21:26:15', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-08 21:26:27', 'statusTwo': 0}, {'duidOne': '5CB7F6892CB4', 'duidTwo': '94C25175C1C4', 'cliente': 'Iqos Canal Indirecto', 'tienda': 'Av. Adolfo Ruiz Cortines 255 Mexico Nuevo Cd L?pez Mateos CP 52977', 'iccid': '895202052349337016', 'imsi': '334020110465963', 'msisdn': '525544414978', 'lastReportTimeOne': '2024-07-09 09:32:10', 'statusOne': 1, 'lastReportTimeTwo': '2024-07-09 09:32:29', 'statusTwo': 1}, {'duidOne': 'D6A14B850428', 'duidTwo': '', 'cliente': 'Iqos Canal directo', 'tienda': 'Acoxpa', 'iccid': '895202002419652029', 'imsi': '334020114368197', 'msisdn': '525550709597', 'lastReportTimeOne': '2024-07-06 10:12:11', 'statusOne': 0, 'lastReportTimeTwo': 'NO', 'statusTwo': 0}, {'duidOne': 'D69365A8B2E4', 'duidTwo': 'F49B026B4EE4', 'cliente': 'Iqos Canal directo', 'tienda': 'Santa Fe 1', 'iccid': '895202002419652033', 'imsi': '334020114368201', 'msisdn': '525550709601', 'lastReportTimeOne': '2024-07-08 21:13:10', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-08 21:13:50', 'statusTwo': 0}, {'duidOne': '61F9400C4128', 'duidTwo': 'DB765F3D6628', 'cliente': 'Iqos Canal directo', 'tienda': 'Santa Fe 2', 'iccid': '895202002419652035', 'imsi': '334020114368204', 'msisdn': '525550709609', 'lastReportTimeOne': '2024-07-08 21:00:21', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-08 21:03:35', 'statusTwo': 0}, {'duidOne': '516B596F2D28', 'duidTwo': 'F8BC59B26628', 'cliente': 'Iqos Canal directo', 'tienda': 'Antara', 'iccid': '895202052349337029', 'imsi': '334020110465976', 'msisdn': '525544552886', 'lastReportTimeOne': '2024-07-09 09:29:45', 'statusOne': 1, 'lastReportTimeTwo': '2024-07-09 09:39:02', 'statusTwo': 1}, {'duidOne': '4AF805C0B228', 'duidTwo': '52E50C570428', 'cliente': 'Iqos Canal directo', 'tienda': 'Claveria', 'iccid': '895202052349337013', 'imsi': '334020110465959', 'msisdn': '525544428855', 'lastReportTimeOne': '2024-07-03 10:50:17', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-03 10:50:18', 'statusTwo': 0}, {'duidOne': 'CA0FDE67D1D0', 'duidTwo': '03BE3D2E78D0', 'cliente': 'Iqos Canal directo', 'tienda': 'Parque Delta', 'iccid': '895202052349337033', 'imsi': '334020110465980', 'msisdn': '525565319550', 'lastReportTimeOne': '2024-07-08 20:59:46', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-08 20:59:48', 'statusTwo': 0}, {'duidOne': '54713B911528', 'duidTwo': '2EED304DF528', 'cliente': 'Iqos Canal directo', 'tienda': 'Manacar', 'iccid': '895202002419652032', 'imsi': '334020114368200', 'msisdn': '525550709593', 'lastReportTimeOne': '2024-07-08 21:14:55', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-08 21:15:28', 'statusTwo': 0}, {'duidOne': '2AA4619E23D0', 'duidTwo': '19FDAB95B1D0', 'cliente': 'Iqos Canal directo', 'tienda': 'Metropoli', 'iccid': '895202052349337028', 'imsi': '334020110465975', 'msisdn': '525544556077', 'lastReportTimeOne': '2024-07-04 10:30:29', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-04 10:30:27', 'statusTwo': 0}, {'duidOne': 'FB0E1219DF28 ', 'duidTwo': '2D42E615C328', 'cliente': 'Iqos Canal directo', 'tienda': 'Mitikah', 'iccid': '895202052349337032', 'imsi': '334020110465979', 'msisdn': '525564895506', 'lastReportTimeOne': 'NO', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-02 13:52:29', 'statusTwo': 0}, {'duidOne': '060A70AA0B28', 'duidTwo': '4.26218E+11', 'cliente': 'Iqos Canal directo', 'tienda': 'Oasis', 'iccid': '895202002419652030', 'imsi': '334020114368198', 'msisdn': '525550709612', 'lastReportTimeOne': '2024-07-08 21:00:40', 'statusOne': 0, 'lastReportTimeTwo': 'NO', 'statusTwo': 0}, {'duidOne': '18209AA7E828', 'duidTwo': '3444DB8D3B28', 'cliente': 'Iqos Canal directo', 'tienda': 'Oceania', 'iccid': '895202052349351971', 'imsi': '334020110490678', 'msisdn': '525620026369', 'lastReportTimeOne': '2024-07-05 21:04:47', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-05 21:04:34', 'statusTwo': 0}, {'duidOne': '8445D88094D0', 'duidTwo': '0D081B2DE9D0', 'cliente': 'Iqos Canal directo', 'tienda': 'Patio Universidad', 'iccid': '895202052349351968', 'imsi': '334020110490671', 'msisdn': '525620026367', 'lastReportTimeOne': '2024-07-02 13:51:48', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-02 13:51:48', 'statusTwo': 0}, {'duidOne': '6E3C462E2B28', 'duidTwo': '4C587CEEEC28', 'cliente': 'Iqos Canal directo', 'tienda': 'Perisur', 'iccid': '895202052349337026', 'imsi': '334020110465973', 'msisdn': '525544592520', 'lastReportTimeOne': '2024-07-02 10:50:13', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-02 10:50:50', 'statusTwo': 0}, {'duidOne': '392AA22F6728', 'duidTwo': '6BFCFBA9C528', 'cliente': 'Iqos Canal directo', 'tienda': 'Portal San Angel', 'iccid': '895202002419652031', 'imsi': '334020114368199', 'msisdn': '525550709605', 'lastReportTimeOne': '2024-07-01 20:56:42', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-01 20:56:05', 'statusTwo': 0}, {'duidOne': '50B648195328', 'duidTwo': 'E0D0E701E328', 'cliente': 'Iqos Canal directo', 'tienda': 'Reforma222', 'iccid': '895202052349337034', 'imsi': '334020110465981', 'msisdn': '525565346732', 'lastReportTimeOne': '2024-07-03 20:54:51', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-03 20:55:47', 'statusTwo': 0}, {'duidOne': '91741BD63528', 'duidTwo': 'CFDDC12F6328', 'cliente': 'Iqos Canal directo', 'tienda': 'Samara', 'iccid': '895202052349337030', 'imsi': '334020110465977', 'msisdn': '525544552555', 'lastReportTimeOne': '2024-07-02 20:53:37', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-02 20:59:23', 'statusTwo': 0}, {'duidOne': '3537339B8728', 'duidTwo': '7603289EC028', 'cliente': 'Iqos Canal directo', 'tienda': 'Santa Fe 3', 'iccid': '895202002419652034', 'imsi': '334020114368203', 'msisdn': '525550709613', 'lastReportTimeOne': '2024-07-08 20:36:09', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-08 20:43:02', 'statusTwo': 0}, {'duidOne': '1928129AD028', 'duidTwo': '645E87D78D28', 'cliente': 'Iqos Canal directo', 'tienda': 'Satelite', 'iccid': '895202052349337022', 'imsi': '334020110465969', 'msisdn': '525544652465', 'lastReportTimeOne': '2024-07-08 20:58:00', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-08 21:00:28', 'statusTwo': 0}, {'duidOne': '88DB2EBBE3D0', 'duidTwo': '615D0CE009D0', 'cliente': 'Iqos Canal directo', 'tienda': 'Toreo', 'iccid': '895202052349337014', 'imsi': '334020110465960', 'msisdn': '525544425720', 'lastReportTimeOne': '2024-07-08 10:25:38', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-08 10:25:45', 'statusTwo': 0}, {'duidOne': '0326043662D0', 'duidTwo': '1FEF20E2A6D0', 'cliente': 'Iqos Canal directo', 'tienda': 'Tezontle', 'iccid': '895202052349337020', 'imsi': '334020110465967', 'msisdn': '525544665810', 'lastReportTimeOne': '2024-07-08 20:59:08', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-08 20:55:32', 'statusTwo': 0}, {'duidOne': 'F99DFBC649D0', 'duidTwo': '8C2926AC59D0', 'cliente': 'Iqos Canal directo', 'tienda': 'Linda Vista', 'iccid': '895202052349337051', 'imsi': '334020110465999', 'msisdn': '525580556883', 'lastReportTimeOne': '2024-07-08 21:00:00', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-08 20:59:47', 'statusTwo': 0}, {'duidOne': '5DB0A4D55328', 'duidTwo': '203CC0B4F828', 'cliente': 'Iqos Canal directo', 'tienda': 'Parque Antenas', 'iccid': '895202052349351973', 'imsi': '334020110490680', 'msisdn': '525620026372', 'lastReportTimeOne': '2024-07-05 11:36:43', 'statusOne': 0, 'lastReportTimeTwo': '2024-07-05 11:36:42', 'statusTwo': 0}]]
# Verificar que la API devolvió datos válidos antes de intentar generar el PDF
print(type(datos_api))
if datos_api:
    resultado = generar_pdf(datos_api)
    print(resultado)
else:
    print("No se pudieron obtener datos de la API")