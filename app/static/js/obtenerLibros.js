// Cuando se haga clic en un botón "Editar"
document.querySelectorAll('.editar-libro-btn').forEach(btn => {
    btn.addEventListener('click', function () {
        const isbn = this.getAttribute('data-isbn');

        // Hacer una llamada AJAX para obtener los detalles del libro
        fetch(`/obtener_libro/${isbn}`)
            .then(response => response.json())
            .then(data => {
                if (data.exito) {
                    // Llenar el modal con la información del libro
                    const libro = data.libro;
                    document.getElementById('tituloM').value = libro.titulo;
                    document.getElementById('ISBNM').value = libro.isbn;
                    document.getElementById('precioM').value = libro.precio;
                    document.getElementById('autorM').value = libro.autor;
                    document.getElementById('apellidoM').value = libro.apellido;
                    document.getElementById('descripcionM').value = libro.descripcion;

                    // Si hay portada, mostrarla en el modal
                    if (libro.portada) {
                        document.getElementById('portadaMPreview').style.display = 'block';
                        document.getElementById('portadaMPreview').src = libro.portada;
                    }
                } else {
                    alert(data.mensaje); // Si no se encuentra el libro
                }
            })
            .catch(error => {
                alert('Error al obtener los datos del libro');
                console.error(error);
            });
    });
});

