function confirmDelete(fileName) {
    event.preventDefault(); // Evita el comportamiento predeterminado del enlace
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    
    Swal.fire({
        title: 'Are you sure?',
        text: 'You will delete ' + fileName + '!',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
        if (result.isConfirmed) {
            // Mostrar el loader
            document.getElementById("loaderContainer").style.display = 'flex';
            // Hacer una solicitud POST al servidor para eliminar el archivo
            fetch('/delete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ selectedItems: [fileName] })
            })
            .then(response => {
                // Mostrar el loader
                document.getElementById("loaderContainer").style.display = 'none';
                if(response.redirected) {
                    window.location.href = response.url; // Redirige a la URL proporcionada por el servidor
                }else{
                    return response.text(); // Si no hay redirección, devuelve el cuerpo de la respuesta como texto
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Mostrar el loader
                document.getElementById("loaderContainer").style.display = 'none';
            });
        }
    });
}

//Modify
document.getElementById("upload-button").addEventListener("click", async function() {
    const { value: formValues } = await Swal.fire({
        title: "Upload File Media",
        html:
            '<input id="swal-input1" class="swal2-input" placeholder="Enter tags separated by commas">' +
            '<label for="file-input" class="custom-file-upload" id="file-label">' +
            '   <i class="fas fa-cloud-upload-alt"></i> Choose File' +
            '</label>' +
            '<input id="file-input" type="file" accept="video/*, image/*">' +
            '<small class="file-message">You have already selected a file.</small>',
        focusConfirm: false,
        preConfirm: () => {
            return [
                document.getElementById("swal-input1").value,
                document.getElementById("file-input").files[0]
            ];
        },
        customClass: {
            confirmButton: 'btn btn-primary-custom',
            cancelButton: 'btn btn-danger'
        },
        showCancelButton: true,
        confirmButtonText: 'Upload',
        cancelButtonText: 'Cancel',
        showLoaderOnConfirm: true,
        allowOutsideClick: () => !Swal.isLoading(),
        didOpen: () => {
            // Añadir evento change al input de archivo
            document.getElementById("file-input").addEventListener("change", function() {
                // Mostrar el texto small si se selecciona un archivo
                if (this.files.length > 0) {
                    document.querySelector(".file-message").style.display = 'inline';
                }
            });
        }
    });

    const tag = formValues[0];
    const file = formValues[1];

    if (file) {
        // Actualizar el texto del botón con el nombre del archivo seleccionado
        document.getElementById("file-label").innerText = file.name;

        const formData = new FormData();
        formData.append("file", file);
        formData.append("tag", tag);

        // Mostrar el loader antes de la solicitud
        Swal.showLoading();

        // Obtener el token CSRF de la metaetiqueta
        const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
        document.getElementById("loaderContainer").style.display = 'flex';
        fetch("/upload_media", {
            method: "POST",
            headers: {
                'X-CSRFToken': csrfToken  // Incluir el token CSRF en los encabezados
            },
            body: formData
        })
        .then(response => {
            // Ocultar el loader después de completar la solicitud
            document.getElementById("loaderContainer").style.display = 'none';
            Swal.close();
            if (response.redirected) {
                window.location.href = response.url; // Redirige a la URL proporcionada por el servidor
            } else {
                return response.text(); // Si no hay redirección, devuelve el cuerpo de la respuesta como texto
            }
        })
        .then(data => {
            if (data) {
                Swal.fire({
                    title: "Server Response",
                    text: data,
                    icon: 'success'
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'There was an error uploading the file.'
            });
        });
    }
});


document.getElementById("delete-button").addEventListener("click", function() {
    console.log("CLICK delete");
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    var selectedItems = [];
    var checkboxes = document.querySelectorAll('.styled-checkbox');
    checkboxes.forEach(function(checkbox) {
        if (checkbox.checked) {
            var name = checkbox.parentElement.parentElement.querySelector('td:nth-child(2)').textContent;
            selectedItems.push(name);
        }
    });
    console.log("CHECKBOXES: ", checkboxes);
    console.log("SELECTED: ", selectedItems);

    // Mostrar el loader
    document.getElementById("loaderContainer").style.display = 'flex';

    // Enviar la lista de elementos seleccionados al servidor
    fetch('/delete', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken  // Incluir el token CSRF en los encabezados
        },
        body: JSON.stringify({selectedItems: selectedItems})
    }).then(function(response) {
        // Ocultar el loader después de completar la solicitud
        document.getElementById("loaderContainer").style.display = 'none';
        // Manejar la respuesta del servidor si es necesario
        if(response.redirected) {
            window.location.href = response.url; // Redirige a la URL proporcionada por el servidor
        }else{
            return response.text(); // Si no hay redirección, devuelve el cuerpo de la respuesta como texto
        }
    }).catch(function(error) {
        // Ocultar el loader si hay un error
        document.getElementById("loaderContainer").style.display = 'none';
        console.error('Error:', error);
    });
});



function loadVideo(wrapper) {
    var video = wrapper.querySelector('video');
    if (!video.src) {
        var source = video.querySelector('source');
        video.src = source.src;
    }
    video.play();
}