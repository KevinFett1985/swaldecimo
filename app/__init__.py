from logging import raiseExceptions

from flask import Flask, request, jsonify
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf.csrf import CSRFProtect
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash #validar contraseñas
from flask_mail import Mail

from werkzeug.utils import secure_filename


from .models.ModeloLibro import ModeloLibro
from .models.ModeloUsuario import ModeloUsuario
from .models.ModeloCompra import ModeloCompra
from .models.entities.Usuario import Usuario, newUsuario
from .models.entities.Compra import Compra
from .models.entities.Libro import Libro, newLibro

from .consts import *
from .emails import confirmacion_compra, confirmacion_registro
app = Flask(__name__)

csrf = CSRFProtect()
db = MySQL(app)
login_manager_app = LoginManager(app)
mail = Mail()


@login_manager_app.user_loader
def load_user(id):
    return ModeloUsuario.Obtener_por_id(db, id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = Usuario(None, request.form['usuario'],
                          request.form['password'], None)
        usuario_logeado = ModeloUsuario.login(db, usuario)
        if usuario_logeado != None:
            login_user(usuario_logeado)
            print("DENTRO")
            flash(MENSAJE_BIENVENIDA, 'success')
            return redirect(url_for('index'))
        else:
            flash(LOGIN_CREDENCIALESINVALIDAES, 'warning')  # usando variable
            print("VOLVER A INGRESAR CRENDENCIALES")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/')
@login_required
def index():
    if current_user.is_authenticated:
        if current_user.tipousuario.id == 1:
            try:
                libros_vendidos= ModeloLibro.listar_libros_vendidos(db)
                data = {
                    'titulo':'Libros Vendidos',
                    'libros_vendidos':libros_vendidos
                }
                return render_template('index.html', data=data)
            except Exception as ex:
                print("error aqui")
                print(ex)
                return render_template('errores/error.html',mensaje=format(ex))
        else:
            try:
                libros=ModeloLibro.listar_libros(db)
                data={
                    'titulo':'Libros Disponibles',
                    'libros':libros
                }
                return render_template('index.html',data=data)
            except Exception as ex:
                 render_template('errores/error.html',mensaje=format(ex))
            
    else:
        return redirect(url_for('login'))


@app.route('/archivo')
@login_required
def archivo():
    if current_user.is_authenticated:
        try:
            libros_editar = ModeloLibro.listar_libros_dos(db)
            data = {
                'titulo': 'Administración libros',
                'libros_editar': libros_editar
            }

            # Itera sobre la lista y accede a los atributos de cada objeto
            for i, libro in enumerate(data['libros_editar']):
                if hasattr(libro, 'isbn') and hasattr(libro, 'nombre') and hasattr(libro, 'descripcion'):
                    print(f"Libro {i}: {libro.isbn}, {libro.nombre}, {libro.descripcion}")
                else:
                    print(f"Error: El elemento en la posición {i} no tiene los atributos esperados. Valor: {libro}")

            return render_template('archivo.html', data=data)
        except Exception as ex:
            print(f"Error: {ex}")
            return render_template('errores/error.html', mensaje=format(ex))
    else:
        return redirect(url_for('login'))


@app.route('/main')
def main():
    try:
        libros = ModeloLibro.listar_libros(db)
        data = {
            'titulo': 'Libros Disponibles',
            'libros': libros
        }
        return render_template('main.html', data=data)
    except Exception as ex:
        print(ex)
        return render_template('errores/error.html', mensaje=format(ex))


@app.route('/libros')
@login_required
def listar_libros():
    try:
        compras = ModeloCompra.listar_compras_usuario(db, current_user)
        data = {
            'titulo':'Mis compras',
            'compras': compras
        }

        return render_template('listado_libros.html', data=data)
    except Exception as ex:
        print("erroraqui")
        print(ex)
        return render_template('errores/error.html',mensaje=format(ex))


@app.route('/register')
def register():
    return render_template('auth/register.html')


@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    data = {}
    try:
        # Obtener datos del formulario
        datos_formulario = request.json
        usuario = datos_formulario.get('usuario')
        password = datos_formulario.get('password')
        direccion = datos_formulario.get('direccion')
        telefono = datos_formulario.get('telefono')
        email = datos_formulario.get('email')
        password_encriptada=generate_password_hash(password)
        print(usuario, password, direccion, telefono, email)

        # Crear un nuevo objeto de usuario
        nuevo_usuario = newUsuario(
            None, usuario, password_encriptada, 2, direccion,telefono, email)

        # Instanciar un objeto de ModeloUsuario
        modelo_usuario = ModeloUsuario()

        # Registrar el nuevo usuario en la base de datos
        data['exito'] = modelo_usuario.registrar_cliente(
            db, usuario=nuevo_usuario)
        if data['exito']:
            data['mensaje'] = 'Usuario registrado correctamente'
            confirmacion_registro(app, mail, nuevo_usuario) 
        else:
            data['mensaje'] = 'Error al registrar el usuario'
    except Exception as ex:
        data['exito'] = False
        data['mensaje'] = str(ex)
    return jsonify(data)


from flask import request, jsonify
from werkzeug.utils import secure_filename
import os
"""
@app.route('/registrar_libro', methods=['POST'])
def registrar_libro():
    data = {}
    try:
        # Obtener datos del formulario
        titulo = request.form.get('titulo')
        ISBN = request.form.get('ISBN')
        precio = request.form.get('precio')
        autor = request.form.get('autor')
        apellido = request.form.get('apellido')
        descripcion = request.form.get('descripcion')
        portada = request.files.get('portada')  # Archivo de portada
        nombreArchivo = request.form.get('nombreArchivo')
        print(ISBN, titulo, apellido, autor, precio, descripcion, portada,nombreArchivo)

        if not portada:
            data['exito'] = False
            data['mensaje'] = 'No se subió ningún archivo de portada.'
            return jsonify(data)

        imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], portada)

        # Asegurarse de que el directorio existe
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Guardar el archivo
        portada.save(imagen_path)

        # Instanciar un objeto de ModeloLibro (ajustar según tu implementación)
        modelo_libro = ModeloLibro()

        # Registrar el libro en la base de datos
        exito = modelo_libro.registrar_libro(
            db, ISBN, titulo, apellido, autor, precio, descripcion, nombreArchivo
        )

        if exito:
            data['exito'] = True
            data['mensaje'] = 'Libro registrado correctamente.'
        else:
            data['exito'] = False
            data['mensaje'] = 'Error al registrar el libro.'

    except Exception as ex:
        data['exito'] = False
        data['mensaje'] = str(ex)

    return jsonify(data)


"""

import mimetypes
import os
from flask import jsonify, request, render_template

UPLOAD_FOLDER = '/home/ubuntu/swaldecimo/app/static/img/portadas'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg','png'}

# Función para verificar extensiones permitidas
def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/registrar_libro', methods=['POST'])
def registrar_libro():
    data = {}
    try:
        # Obtener datos del formulario
        titulo = request.form.get('titulo')
        ISBN = request.form.get('ISBN')
        precio = request.form.get('precio')
        autor = request.form.get('autor')
        apellido = request.form.get('apellido')
        descripcion = request.form.get('descripcion')
        portada = request.files.get('portada')  # Archivo de portada
        nombreArchivo = request.form.get('nombreArchivo')
        print(ISBN, titulo, apellido, autor, precio, descripcion, portada, nombreArchivo)
        print(type(ISBN), type(titulo), type(apellido), type(autor), type(precio), type(descripcion), type(portada),
              type(nombreArchivo))

        if not portada or portada.filename == '':
            data['exito'] = False
            data['mensaje'] = 'No se subió ningún archivo de portada.'
            return jsonify(data)

        # Validar archivo de portada
        if allowed_file(portada.filename):
            mime_type, _ = mimetypes.guess_type(portada.filename)
            if mime_type == 'image/jpeg':
                # Guardar el archivo de portada
                filename = portada.filename
                imagen_path = os.path.join(UPLOAD_FOLDER, filename)

                # Asegurarse de que el directorio existe
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                portada.save(imagen_path)
            else:
                data['exito'] = False
                data['mensaje'] = 'El archivo no es un tipo de imagen válido.'
                return jsonify(data)
        else:
            data['exito'] = False
            data['mensaje'] = 'La extensión del archivo no está permitida.'
            return jsonify(data)

        # Instanciar un objeto de ModeloLibro (ajustar según tu implementación)
        modelo_libro = ModeloLibro()

        # Registrar el libro en la base de datos
        exito = modelo_libro.registrar_libro(
            db, ISBN, titulo, apellido, autor, precio, descripcion, nombreArchivo
        )

        if exito:
            data['exito'] = True
            data['mensaje'] = 'Libro registrado correctamente.'
        else:
            data['exito'] = False
            data['mensaje'] = 'Error al registrar el libro.'


    except Exception as ex:
        data['exito'] = False
        data['mensaje'] = f'Error: {str(ex)}'

    return jsonify(data)

@app.route('/modificar_libro', methods=['POST'])
def modificar_libro():
    data = {}
    try:
        # Obtener datos del formulario
        titulo = request.form.get('titulo')
        ISBN = request.form.get('ISBN')
        precio = request.form.get('precio')
        autor = request.form.get('autor')
        apellido = request.form.get('apellido')
        descripcion = request.form.get('descripcion')
        portada = request.files.get('portada')  # Archivo de portada
        nombreArchivo = request.form.get('nombreArchivo')  # Nombre del archivo anterior

        print(ISBN, titulo, apellido, autor, precio, descripcion, portada, nombreArchivo)

        # Validación de campos obligatorios
        if not all([ISBN, titulo, precio, autor, apellido, descripcion]):
            return jsonify({"exito": False, "mensaje": "Faltan datos obligatorios."})

        # Validación del precio
        try:
            precio = float(precio)  # Asegúrate de que sea un número válido
        except ValueError:
            return jsonify({"exito": False, "mensaje": "El precio debe ser un número válido."})

        # Validación y manejo del archivo de portada
        if portada and portada.filename != '':
            if allowed_file(portada.filename):  # Valida el tipo de archivo
                filename = secure_filename(portada.filename)
                imagen_path = os.path.join(UPLOAD_FOLDER, filename)

                # Crear el directorio si no existe
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)

                # Guardar la nueva portada
                portada.save(imagen_path)
                nombreArchivo = filename  # Actualizar el nombre del archivo
            else:
                return jsonify({"exito": False, "mensaje": "La extensión del archivo no está permitida."})

        # Instanciar el modelo y llamar a la función para modificar el libro
        modelo_libro = ModeloLibro()
        exito = modelo_libro.modificar_libro(
            db, ISBN, titulo, apellido, autor, precio, descripcion, nombreArchivo
        )
        print(descripcion)
        if exito:
            data['exito'] = True
            data['mensaje'] = 'Libro modificado correctamente.'
        else:

            data['exito'] = False
            data['mensaje'] = 'Error al modificar el libro en la base de datos.'

    except Exception as ex:
        print(f"Error al modificar el libro: {str(ex)}")  # Log para depuración
        data['exito'] = False
        data['mensaje'] = f"Error inesperado: {str(ex)}"

    return jsonify(data)


@app.route('/comprarLibro', methods=['POST'])
@login_required
def comprar_libro():
    data_request = request.get_json()
    data = {}
    try:
        libro = ModeloLibro.leer_libro(db, data_request['isbn'])
        # libro=Libro(data_request['isbn'], None, None,None, None)
        compra = Compra(None, libro, current_user)
        data['exito'] = ModeloCompra.registrar_compra(db, compra)
        # confirmacion_compra(mail, current_user, libro) envio sincrono
        confirmacion_compra(app, mail, current_user, libro)  # encio async
    except Exception as ex:
        data['mensaje'] = format(ex)
        data['exito'] = False
    return jsonify(data)

@app.route('/logout')
def logout():
    logout_user()
    flash(LOGOUT, 'success')  # usando variable
    return redirect(url_for('login'))

def pagina_no_encontrada(errores):
    print(errores)
    return render_template('errores/404.html'), 404

def pagina_no_autorizada(error):
    print(error)
    return redirect(url_for('login'))

# Define the upload folder path directly

import os
@app.route('/subir', methods=['POST'])
@csrf.exempt
def subir():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        # Save the file directly to the specified folder
        filename = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        return render_template('success.html')

import mimetypes
ALLOWED_EXTENSIONS = {'jpg', 'jpeg','png'}

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/subirseguro', methods=['POST'])
@csrf.exempt
def subirseguro():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        # Check MIME type to be sure it is an image/jpeg
        mime_type, _ = mimetypes.guess_type(file.filename)
        if mime_type == 'image/jpeg':
            filename = file.filename
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            return render_template('success.html')
        else:
            return render_template('nosuccess.html')
    else:
        return render_template('nosuccess.html')


from flask import jsonify

@app.route('/eliminar_libro', methods=['POST'])
def eliminar_libro():
    data = {}
    try:
        # Obtener el ISBN del cuerpo de la solicitud
        request_data = request.get_json()
        ISBN = request_data.get('ISBN')

        # Validar que el ISBN esté presente
        if not ISBN:
            return jsonify({"exito": False, "mensaje": "Falta el ISBN del libro a eliminar."})
        print("ESTE ES EL ISBN" + ISBN)
        # Instanciar el modelo y llamar a la función para eliminar el libro
        modelo_libro = ModeloLibro()
        exito = modelo_libro.eliminar_libro(db, ISBN)

        if exito:
            data['exito'] = True
            data['mensaje'] = 'Libro no eliminado correctamente.'
        else:
            data['exito'] = False
            data['mensaje'] = 'Libro eliminado correctamente'
        print(exito)
    except Exception as ex:
        print(f"Error al eliminar el libro: {str(ex)}")  # Log para depuración
        data['exito'] = False
        data['mensaje'] = f"Error inesperado: {str(ex)}"

    return jsonify(data)


def inicializar_app(config):
    app.config.from_object(config)
    csrf.init_app(app)
    mail.init_app(app)
    app.register_error_handler(404, pagina_no_encontrada)
    app.register_error_handler(401, pagina_no_autorizada)
    return app
