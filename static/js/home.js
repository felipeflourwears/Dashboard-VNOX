function popupSuccess(message) {
    Swal.fire({
        position: 'center',
        icon: 'success',
        title: message,
        showConfirmButton: false,
        timer: 1500
    });
}

function confirmDelete(event) {
    event.preventDefault(); // Evita el comportamiento predeterminado del enlace
    const url = event.target.href; // Obtiene la URL del enlace

    Swal.fire({
        title: 'Are you sure?',
        text: 'You will reset this player!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, reset it!'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = url; // Redirige a la URL si se confirma la eliminación
        }
    });
}


function confirmServer(event) {
    event.preventDefault(); // Evita el comportamiento predeterminado del enlace
    const url = event.target.href; // Obtiene la URL del enlace

    Swal.fire({
        title: 'Are you sure?',
        text: 'This order will be attended to',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, serve it!'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = url; // Redirige a la URL si se confirma la eliminación
        }
    });
}

function openPopupMail(event) {
    event.preventDefault();

    Swal.fire({
        title: "Enter your email address",
        input: "email",
        inputAttributes: {
            autocapitalize: "off"
        },
        showCancelButton: true,
        confirmButtonText: "Send Report",
        allowOutsideClick: () => !Swal.isLoading(),
    }).then((result) => {
        if (result.isConfirmed) {
            const email = result.value;

            if (!email || email.trim() === "") {
                Swal.fire({
                    title: "Invalid email address",
                    icon: "error"
                });
                return;
            }

            fetch(`/send_report?email=${email}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Request failed with status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log(data);  // Imprime la respuesta del servidor en la consola

                    if (data && data.success) {
                        Swal.fire({
                            title: "Report sent successfully!",
                            icon: "success"
                        });
                    } else {
                        Swal.fire({
                            title: "Error sending report",
                            text: data && data.message ? data.message : "Unknown error",
                            icon: "error"
                        });
                    }
                })
                .catch(error => {
                    Swal.fire({
                        title: "Error sending report",
                        text: error.message,
                        icon: "error"
                    });
                });
        } else if (result.isDenied) {
            Swal.fire({
                title: "Canceled",
                icon: "info"
            });
        }
    });
}
