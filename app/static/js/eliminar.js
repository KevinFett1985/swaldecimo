(function () {
    // Seleccionar todos los botones de eliminar
    document.querySelectorAll('[data-bs-toggle="modal"]').forEach(button => {
        button.addEventListener('click', function () {
            // Obtener el ISBN del libro desde el atributo value
            const libroId = this.value;
            console.log('ISBN del libro:', libroId);  // Verifica si se obtiene correctamente

            // Agregar el ISBN al botón de confirmación dentro del modal
            const eliminarButton = document.querySelector(`#eliminarLibro${libroId}`);
            if (eliminarButton) {
                eliminarButton.setAttribute('data-id', libroId);  // Asignar el ISBN al botón de confirmación
            }
        });
    });

    // Manejar la acción de confirmación de eliminación
    document.querySelectorAll('.btn-danger[data-id]').forEach(eliminarButton => {
        eliminarButton.addEventListener('click', async function () {
            // Obtener el ISBN del elemento a eliminar
            const libroId = this.getAttribute('data-id');
            console.log('Confirmación ISBN:', libroId); // Verifica si el ISBN está bien asignado

            const csrf_token = document.querySelector("[name='csrf_token']").value;

            try {
                const response = await fetch(`${window.origin}/eliminar_libro`, {
                    method: 'POST',
                    mode: 'same-origin',
                    credentials: 'same-origin',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRF-TOKEN': csrf_token
                    },
                    body: JSON.stringify({ ISBN: libroId })
                });

                if (!response.ok) {
                    const errorMessage = await response.text();
                    notificacionSwal('Error', errorMessage, 'error', 'OK');
                    return;
                }

                const data = await response.json();
                if (data && data.exito) {
                    // Mostrar mensaje de éxito
                    notificacionSwal('Éxito', 'Libro eliminado exitosamente', 'success', 'OK');

                    // Eliminar el libro de la interfaz sin recargar la página
                    const libroElemento = document.querySelector(`#EliminarLibro${libroId}`);
                    if (libroElemento) {
                        libroElemento.closest('tr').remove(); // Elimina la fila del libro en la tabla
                    }

                    // Cerrar el modal
                    const modal = document.querySelector(`#confirmarEliminarModal${libroId}`);
                    if (modal) {
                        const modalInstance = new bootstrap.Modal(modal);
                        modalInstance.hide();
                    }

                } else {
                    notificacionSwal('Éxito', 'Libro eliminado exitosamente', 'success', 'OK');
                    setTimeout(function () {
                    location.reload(); // Recarga la página actual
                }, 3000);
                    }
            } catch (error) {
                console.error('Error al procesar la solicitud:', error);
                notificacionSwal('Error', 'No se pudo procesar la solicitud', 'error', 'OK');
            }
        });
    });
})();
