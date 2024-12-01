(function () {
    const registroButton = document.getElementById('RegistrarLibro');
    const csrf_token = document.querySelector("[name='csrf_token']").value;

    // Flag para evitar envíos múltiples
    let enProceso = false;

    // Función manejadora del evento click
    async function registrarLibroHandler(event) {
        event.preventDefault(); // Evitar el comportamiento de envío predeterminado

        // Si ya está en proceso, no hacer nada
        if (enProceso) {
            console.log('Ya se está procesando el formulario. Espera...');
            return;
        }

        // Activar la bandera y desactivar el botón
        enProceso = true;
        registroButton.disabled = true;

        // Remover el listener para evitar futuros clics
        registroButton.removeEventListener('click', registrarLibroHandler);

        // Obtener los valores del formulario
        const titulo = document.getElementById('titulo').value;
        const ISBN = document.getElementById('ISBN').value;
        const precio = document.getElementById('precio').value;
        const autor = document.getElementById('autor').value;
        const apellido = document.getElementById('apellido').value;
        const descripcion = document.getElementById('descripcion').value;
        const portada = document.getElementById('portada').files[0]; // Archivo
        const nombreArchivo = portada ? portada.name : ''; // Nombre del archivo
        console.log(descripcion)
        // Validación de los datos
        if (!validarExpresionesRegulares(titulo, ISBN, precio, autor, apellido, descripcion)) {
            console.log('Validación fallida.');
            registroButton.disabled = false; // Reactivar el botón
            enProceso = false; // Resetear flag
            registroButton.addEventListener('click', registrarLibroHandler); // Volver a agregar el listener si la validación falla
            return;
        }

        // Crear el FormData
        const formData = new FormData();
        formData.append('titulo', titulo);
        formData.append('ISBN', ISBN);
        formData.append('precio', precio);
        formData.append('autor', autor);
        formData.append('apellido', apellido);
        formData.append('descripcion', descripcion);
        formData.append('nombreArchivo', nombreArchivo);

        if (portada) {
            formData.append('portada', portada);
        }

        // Enviar la solicitud
        try {
            const response = await fetch(`${window.origin}/registrar_libro`, {
                method: 'POST',
                mode: 'same-origin',
                credentials: 'same-origin',
                headers: {
                    'X-CSRF-TOKEN': csrf_token
                },
                body: formData
            });

            if (!response.ok) {
                const errorMessage = await response.text();
                notificacionSwal('Error', errorMessage, 'error', 'OK');
                // Si hay error, permitir que el usuario intente de nuevo
                registroButton.disabled = false;
                enProceso = false;
                registroButton.addEventListener('click', registrarLibroHandler); // Volver a agregar el listener
            } else {
                const data = await response.json();
                if (data.exito) {
                    notificacionSwal('Éxito', 'Libro registrado exitosamente', 'success', 'OK');
                    setTimeout(function () {
                    location.reload(); // Recarga la página actual
                }, 2000);
                } else {
                    notificacionSwal('Error', data.mensaje, 'error', 'OK');
                    registroButton.disabled = false;
                    enProceso = false;
                    registroButton.addEventListener('click', registrarLibroHandler); // Volver a agregar el listener si falla el registro
                }
            }
        } catch (error) {
            console.error('Error al procesar la solicitud:', error);
            notificacionSwal('Error', 'No se pudo procesar la solicitud', 'error', 'OK');
            registroButton.disabled = false;
            enProceso = false;
            registroButton.addEventListener('click', registrarLibroHandler); // Volver a agregar el listener en caso de error
        }
    }

    // Asigna el evento una sola vez
    registroButton.addEventListener('click', registrarLibroHandler);
})();
