(function () {
    const registroButton = document.getElementById('registroButton');
    const csrf_token = document.querySelector("[name='csrf_token']").value;

    registroButton.addEventListener('click', async function (event) {
        event.preventDefault();

        const usuario = document.getElementById('usuario').value;
        const email = document.getElementById('email').value;
        const direccion = document.getElementById('direccion').value;
        const telefono = document.getElementById('telefono').value;
        const password = document.getElementById('password').value;
        const password_repeat = document.getElementById('password_repeat').value;


        // Validar expresiones regulares
        if (!validarExpresionesRegulares(usuario, password, email, direccion, telefono, password_repeat)) {
            return false;
        }


        try {
            const response = await fetch(`${window.origin}/registrar_usuario`, {
                method: 'POST',
                mode: 'same-origin',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRF-TOKEN': csrf_token
                },
                body: JSON.stringify({
                    usuario: usuario,
                    email: email,
                    direccion: direccion,
                    telefono: telefono,
                    password: password
                })
            });

            if (!response.ok) {
                const errorMessage = await response.text();
                notificacionSwal('Error', errorMessage, 'error', 'OK');
                return;
            }

            const data = await response.json();
            if (data.exito) {
                notificacionSwal('Éxito', 'Usuario registrado exitosamente', 'success', 'OK');

                // Redirigir al usuario al login de la aplicación después de un breve retraso
                // Espera 3000 milisegundos (3 segundos) antes de redirigir a la página de inicio de sesión
                setTimeout(function () {
                    window.location.href = '/login'; // Redirige a la página de inicio de sesión
                }, 3000); // 3000 milisegundos = 3 segundos

            }

            else {
                notificacionSwal('Error', data.mensaje, 'error', 'OK');
            }
        } catch (error) {
            console.error('Error al procesar la solicitud:', error);
        }
    });



})();

function validarExpresionesRegulares(usuario, password, email, direccion, telefono, password_repeat) {
    // Expresiones regulares para validar los campos
    var usuarioRegex = /^[a-zA-Z0-9_-]{3,16}$/;
    var passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{5,8}$/;
    var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    var direccionRegex = /^[a-zA-Z0-9\s,.'-]{3,}$/;
    var telefonoRegex = /^\d{10}$/;

    // Validar cada campo con su expresión regular correspondiente
    if (!usuarioRegex.test(usuario) && usuario == "") {

        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Usuario inválido",
        });
        return false;
    }

    if (!passwordRegex.test(password)) {
        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Password inválido",
        });
        return false;
    }

    if (!emailRegex.test(email)) {
        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Email inválido",
        });
        return false;
    }

    if (!direccionRegex.test(direccion)) {
        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Dirección inválida",
        });
        return false;
    }

    if (!telefonoRegex.test(telefono)) {
        Swal.fire({
            icon: "error",
            title: "Oops...",
            text: "Teléfono inválido",
        });
        return false;
    }
    if (password !== password_repeat) {
        notificacionSwal('Error', 'Las contraseñas no coinciden', 'error', 'OK');
        return false;
    }

    // Devolver true si todos los campos son válidos
    return true;
}