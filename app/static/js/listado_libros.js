(function () {
    const btnComprarLibro = document.querySelectorAll('.btnComprarLibro');
    let isbnLibroSeleccionado = null;
    const csrf_token = document.querySelector("[name='csrf-token']").value;
    btnComprarLibro.forEach((btn) => {
        btn.addEventListener('click', function () {
            isbnLibroSeleccionado = this.id;
            confirmarCompra();
        });
    });
    const confirmarCompra = () => {
        const textoConfirmacion = 'Comprar';
        Swal.fire({
            title: '¿Confirmar la compra del libro seleccionado?',
            inputAttributes: {
                autocapitalize: 'off'
            },
            showCancelButton: true,confirmButtonText: textoConfirmacion,
            showLoaderOnConfirm: true,
            preConfirm: async () => {
                try {
                    console.log(window.origin)
                    const response = await fetch(`${window.origin}/comprarLibro`, {
                        method: 'POST',
                        mode: 'same-origin',
                        credentials: 'same-origin',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRF-TOKEN': csrf_token
                        },
                        body: JSON.stringify({
                            'isbn': isbnLibroSeleccionado
                        })
                    });/// Carlos Daniel Olivares Sotelo
                    if (!response.ok) {
                        notificacionSwal('Error en la respuesta:', response.statusText, 'error', 'Ok!');
                        return;
                    }
                    const data = await response.json();
                    if(data.exito){
                           notificacionSwal('Éxito', 'Libro comprado', 'success', 'OK!');
                           //FUNCION DEL TIEMPO Y MANDA 
                           setTimeout(function() {
                            // Dentro de la función anónima, establecemos la nueva ubicación de la ventana a la URL '/libros'.
                            window.location.href = '/libros';
                        }, 2000);
                    }else{
                        notificacionSwal('Alerta', data.mensaje, 'warning', 'OK!');

                    }
                } catch (error) {
                    console.error('Error al procesar la solicitud:', error);
                }
            },
            allowOutsideClick: () => false,
            allowEscapeKey: () => false
        });
    };
   
})();
