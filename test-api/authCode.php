<?php
    // Definir el tipo de contenido esperado
    header('Content-Type: application/json');

    // Validar el método de la solicitud
    if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
        echo json_encode([
            'success' => false,
            'message' => 'Método no permitido.'
        ]);
        exit;
    }

    // Leer el cuerpo de la solicitud
    $body = json_decode(file_get_contents('php://input'), true);

    // Validar la presencia de datos
    if (!isset($body['correo']) || !isset($body['token'])) {
        echo json_encode([
            'success' => false,
            'message' => 'Faltan datos en el body.'
        ]);
        exit;
    }

    // Obtener el correo y el token
    $correo = $body['correo'];
    $token = $body['token'];

    enviarToken($correo, $token);

    // Responder con éxito
    echo json_encode([
        'success' => true,
        'message' => 'Datos recibidos y procesados correctamente.'
    ]);

    // Función para enviar el token por correo electrónico
    function enviarToken($correo, $token) {
        $to = $correo;
        $subject = 'Authentication Code';

        // Definir el estilo del correo
        $backgroundColor = '#f2f2f2'; // Color de fondo gris claro
        $primaryColor = '#007bff'; // Color principal azul
        $fontFamily = 'Arial, sans-serif'; // Fuente

        $message = '
        <html>
        <head>
            <style>
                body {
                    background-color: '.$backgroundColor.';
                    font-family: '.$fontFamily.';
                }
        
                h1 {
                    color: '.$primaryColor.';
                    font-size: 24px;
                    margin-top: 0;
                }
        
                p {
                    font-size: 16px;
                    line-height: 1.5;
                }
        
                .token {
                    background-color: '.$primaryColor.';
                    color: #fff;
                    padding: 10px;
                    border-radius: 5px;
                    font-size: 18px;
                    font-weight: bold;
                    width: fit-content;
                    margin: 0 auto;
                }
        
                img {
                    max-width: 300px;
                    height: auto;
                    display: block;
                    margin: 20px auto;
                }
            </style>
        </head>
        <body>
            <h1>Hello!</h1>
            <p>Here is your authentication token:</p>
            <p class="token">' . $token . '</p>
            <p>This token allows you to access to CMSI Popatelier.</p>
            <p>Please keep it in a safe place.</p>
            <img src="https://retailmibeex.net/retailmi_composer/images-page/popnav.png" alt="Image">
        </body>
        </html>
        ';
        // Encabezados del correo
        $headers = 'From: noreply@popcmsi.com' . "\r\n";
        $headers .= 'Content-Type: text/html; charset=UTF-8' . "\r\n";

        // Envío del correo
        $success = mail($correo, $subject, $message, $headers);

        if ($success) {
            echo "Correo enviado con éxito.\n";
        } else {
            echo "Error al enviar el correo.\n";
        }
    }
?>