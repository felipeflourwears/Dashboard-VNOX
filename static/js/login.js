// Mostrar el campo de código de verificación al hacer clic en el botón "Send code"
document.getElementById('send-code-btn').addEventListener('click', function() {
    document.getElementById('code-input').style.display = 'block';
});

// Habilitar el botón de envío cuando se ingresa el código de verificación
document.getElementById('code').addEventListener('input', function() {
    var code = this.value.trim(); // Obtener el valor del campo y eliminar espacios en blanco
    var submitBtn = document.getElementById('submit-btn');

    // Habilitar el botón de envío si el código no está vacío
    if (code) {
        submitBtn.removeAttribute('disabled');
    } else {
        submitBtn.setAttribute('disabled', 'disabled');
    }
});

$(document).ready(function() {
    $("#send-code-btn").click(function() {
        var email = $("#correo").val();
        var csrf_token = $('meta[name="csrf-token"]').attr('content');

        $.ajax({
            url: '/send_code',
            type: 'POST',
            headers: {
                'X-CSRF-TOKEN': csrf_token
            },
            data: {
                email: email
            },
            success: function(response) {
                // Handle success response here
                console.log(response);
            },
            error: function(xhr, status, error) {
                // Handle error response here
                console.error(xhr.responseText);
            }
        });
    });
});

