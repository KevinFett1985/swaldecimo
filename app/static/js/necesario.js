document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".btnComprarLibro").forEach(button => {
        button.addEventListener("click", function() {
            // Verificar si el usuario está autenticado (esto es solo un ejemplo)
            var usuarioAutenticado = false; // Supongamos que el usuario no está autenticado
            
            if (usuarioAutenticado) {
                // Si el usuario está autenticado, realizar la acción de compra
                realizarCompra();
            } else {
                // Si el usuario no está autenticado, mostrar mensaje y botones para iniciar sesión o registrarse
                var mensaje = "Por favor, inicia sesión o regístrate para comprar.";
                mostrarMensaje(mensaje);
            }
        });
    });

    function mostrarMensaje(mensaje) {
        const titleText = '¡Atención!';
        const htmlContent = '<div style="text-align: left;">' + mensaje + '</div>';
        const confirmButtonText = 'OK';
        const loginUrl = document.getElementById('login-url').value;
        const registerUrl = document.getElementById('register-url').value;
      
        Swal.fire({
            title: titleText,
            html: mensaje,
            icon: 'info',
            showCloseButton: true,
            showCancelButton: false,
            showConfirmButton: false,
            footer: '<a class="btn btn-success mr-3" href="' + loginUrl + '">Iniciar sesión</a>' +
            '<a class="btn btn-success ml-3" href="' + registerUrl + '">Registrarse</a>'
        });
    }

    function realizarCompra() {
        // Aquí puedes implementar la lógica para realizar la compra
        const titleText = '¡Compra realizada con éxito!';
        const text = '';
        const icon = 'success';
        const confirmButtonText = 'OK';
        
        Swal.fire({
            title: titleText,
            text: text,
            icon: icon,
            confirmButtonText: confirmButtonText,
            showCloseButton: true
        });
    }
});
