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
