(function () {
    // Seleccionar todos los botones cuyo ID comienza con 'ModificarLibro'
    document.querySelectorAll('[id^="ModificarLibro"]').forEach(button => {
        button.addEventListener('click', async function (event) {
            event.preventDefault();

            // Obtener el índice del botón para identificar el modal correspondiente
            const index = this.id.replace('ModificarLibro', '');

            // Obtener los valores de los campos correspondientes en el modal
            const titulo = document.getElementById(`titulo${index}`).value;
            const ISBN = document.getElementById(`ISBN${index}`).value;
            const precio = document.getElementById(`precio${index}`).value;
            const autor = document.getElementById(`autor${index}`).value;
            const apellido = document.getElementById(`apellido${index}`).value;
            const descripcion = document.getElementById(`descripcion${index}`).value;
            const portadaInput = document.getElementById(`portada${index}`);
            const portada = portadaInput ? portadaInput.files[0] : null; // Obtener archivo si existe
            const nombreArchivo = portada ? portada.name : ''; // Obtener el nombre del archivo o vacío

            console.log({ titulo, ISBN, precio, autor, apellido, descripcion, nombreArchivo });

            // Validar expresiones regulares
            if (!validarExpresionesRegulares(titulo, ISBN, precio, autor, apellido, descripcion)) {
                return; // Detener si la validación falla
            }

            // Crear un objeto FormData para enviar datos y archivo
            const formData = new FormData();
            formData.append('titulo', titulo);
            formData.append('ISBN', ISBN);
            formData.append('precio', precio);
            formData.append('autor', autor);
            formData.append('apellido', apellido);
            formData.append('descripcion', descripcion);
            formData.append('nombreArchivo', nombreArchivo);

            if (portada) {
                formData.append('portada', portada); // Adjunta el archivo solo si existe
            }

            // Obtener el CSRF token
            const csrf_token = document.querySelector("[name='csrf_token']").value;

            try {
                const response = await fetch(`${window.origin}/modificar_libro`, {
                    method: 'POST',
                    mode: 'same-origin',
                    credentials: 'same-origin',
                    headers: {
                        'X-CSRF-TOKEN': csrf_token // CSRF token para proteger la solicitud
                    },
                    body: formData // Usa FormData para el envío
                });

                if (!response.ok) {
                    const errorMessage = await response.text();
                    notificacionSwal('Error', errorMessage, 'error', 'OK');
                    return;
                }

                const data = await response.json();
                if (data.exito) {
                    notificacionSwal('Éxito', 'Libro modificado exitosamente', 'success', 'OK');
                   setTimeout(function () {
                    location.reload(); // Recarga la página actual
                }, 3000);
                } else {
                    notificacionSwal('Error', data.mensaje, 'error', 'OK');
                }
            } catch (error) {
                console.error('Error al procesar la solicitud:', error);
                notificacionSwal('Error', 'No se pudo procesar la solicitud', 'error', 'OK');
            }
        });
    });
})();

// Función para validar expresiones regulares (sin cambios)
function validarExpresionesRegulares(titulo, ISBN, precio, autor, apellido, descripcion) {
    const regexTitulo = /^[a-zA-Z0-9\s,.\-()'"!?¿¡:;#&%+@]{1,255}$/;
    const regexPrecio = /^\d+(\.\d{1,2})?$/; // Permitimos hasta 2 decimales
    const regexAutor = /^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ'`\-.\s]+$/;
    const regexApellido = /^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ'`\-.\s]+$/;
    const regexDescripcion = /^[a-zA-Z0-9\s,.\-()'"!?¿¡:;#&%+@]{10,500}$/;

    if (!regexTitulo.test(titulo)) {
        Swal.fire({ icon: "error", title: "Oops...", text: "Título inválido" });
        return false;
    }

    if (!precio || !regexPrecio.test(precio)) {
        Swal.fire({ icon: "error", title: "Oops...", text: "Precio inválido. Asegúrese de usar un formato válido (ej. 10.99)" });
        return false;
    }

    if (!regexAutor.test(autor)) {
        Swal.fire({ icon: "error", title: "Oops...", text: "Autor inválido" });
        return false;
    }

    if (!regexApellido.test(apellido)) {
        Swal.fire({ icon: "error", title: "Oops...", text: "Apellido inválido" });
        return false;
    }

    if (!regexDescripcion.test(descripcion)) {
        Swal.fire({ icon: "error", title: "Oops...", text: "Descripción inválida. Debe tener entre 10 y 500 caracteres" });
        return false;
    }

    return true; // Si todo está correcto
}
