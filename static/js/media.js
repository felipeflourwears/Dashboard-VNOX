function confirmDelete(event) {
    event.preventDefault(); // Evita el comportamiento predeterminado del enlace
    const url = event.target.href; // Obtiene la URL del enlace

    Swal.fire({
        title: 'Are you sure?',
        text: 'You will delete this media!',
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

