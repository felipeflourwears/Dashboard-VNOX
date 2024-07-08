function openPopupMail(event) {
    event.preventDefault();
    console.log('ENTRADO AL SWAL')
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');


    Swal.fire({
        title: 'Ingrese un dato:',
        input: 'text',
        inputAttributes: {
            autocapitalize: 'off'
        },
        showCancelButton: true,
        confirmButtonText: 'Enviar',
        showLoaderOnConfirm: true,
        preConfirm: (dato) => {
            return fetch('/send_report', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken  // Incluir el token CSRF en los encabezados
                },
                body: new URLSearchParams({
                    'emails': dato
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(response.statusText)
                }
                return response.json();
            })
            .catch(error => {
                Swal.showValidationMessage(
                    `Hubo un error al enviar los datos: ${error}`
                )
            });
        },
        allowOutsideClick: () => !Swal.isLoading()
    }).then((result) => {
        if (result.isConfirmed) {
            Swal.fire(
                '¡Enviado!',
                'Los datos fueron enviados correctamente.',
                'success'
            )
        }
    })
}
