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
