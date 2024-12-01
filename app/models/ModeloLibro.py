from flask import render_template

from .entities.Autor import Autor
from .entities.Libro import Libro
from .entities.Libro import newLibro

class ModeloLibro():
    @classmethod
    def listar_libros(self,db):
        try:
            cursor = db.connection.cursor()
            #sql="SELECT id, titulo, anoedicion FROM libro ORDER BY titulo ASC"
            sql="""SELECT LIB.isbn, LIB.titulo, LIB.portada, LIB.precio, 
                    AUT.apellidos, AUT.nombres 
                    FROM libro LIB JOIN autor AUT ON LIB.autor_id =AUT.id
                    ORDER BY LIB.titulo ASC"""
            cursor.execute(sql)
            data=cursor.fetchall()
            libros=[]
            for row in data:
                aut=Autor(0,row[4],row[5])
                lib=Libro(row[0], row[1], aut, row[2], row[3])
                libros.append(lib)
            return libros
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def listar_libros_dos(self, db):
        try:
            cursor = db.connection.cursor()
            # sql="SELECT id, titulo, anoedicion FROM libro ORDER BY titulo ASC"
            sql = """SELECT LIB.isbn, LIB.titulo, 
                    AUT.apellidos, AUT.nombres, LIB.precio,  LIB.descripcion, LIB.portada
                    FROM libro LIB JOIN autor AUT ON LIB.autor_id =AUT.id
                    ORDER BY LIB.titulo ASC"""
            cursor.execute(sql)
            data = cursor.fetchall()
            libros = []
            for row in data:
                lib = newLibro(row[1], row[0], row[4], row[3], row[2], row[5], row[6])  # Ajuste al orden correcto
                libros.append(lib)
                print(row)
            return libros
        except Exception as ex:
            raise Exception(ex)


    @classmethod 
    def leer_libro(cls, db, isbn):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT isbn, titulo, precio
                    FROM libro WHERE isbn = '{0}'""".format(isbn)
            cursor.execute(sql)
            data = cursor.fetchone()  # Obtiene la primera fila de resultados
            # Verifica si se encontró algún resultado
            if data:
                # Crea un objeto Libro con los datos obtenidos de la consulta
                libro = Libro(data[0], data[1], None, None, data[2])
                return libro
            else:
                # Si no se encuentra ningún libro con el ISBN proporcionado, devuelve None
                return None
        except Exception as ex:
            # Captura cualquier excepción y la eleva para manejarla en un nivel superior
            raise Exception(ex)

    @classmethod    
    def listar_libros_vendidos(self, db):
        try:
            cursor = db.connection.cursor()
            """sql=SELECT COM.libro_isbn, LIB.titulo, LIB.precio, 
            COUNT(COM.libro_isbn) AS Unidades_vendidas
            FROM compra COM JOIN libro LIB ON COM.libro_isbn = LIB.ISBN
            GROUP BY COM.libro_isbn ORDER BY 4 DESC, 2 ASC"""
            sql="""SELECT COM.libro_isbn, LIB.titulo, LIB.precio, 
            COUNT(COM.libro_isbn) AS Unidades_vendidas
            FROM compra COM
            JOIN libro LIB ON COM.libro_isbn = LIB.ISBN
            GROUP BY COM.libro_isbn, LIB.titulo, LIB.precio
            ORDER BY Unidades_vendidas DESC, LIB.titulo ASC;"""

            cursor.execute(sql)
            data=cursor.fetchall()
            libros=[]
            for row in data:
                lib=Libro(row[0], row[1],None,None,row[2])
                lib.unidades_vendidas=int(row[3])
                libros.append(lib)
            return libros
        except Exception as ex:
            raise Exception(ex)



    @classmethod
    def registrar_libro(self, db, isbn, titulo, apellidos, nombres, precio, descripcion, portada):

        try:
            cursor = db.connection.cursor()

            # Llamada al procedimiento almacenado
            cursor.execute('CALL registrar_libro(%s, %s, %s, %s, %s, %s, %s)',
                           (isbn, titulo, apellidos, nombres, precio, descripcion, portada))
            db.connection.commit()  # Confirmar los cambios en la base de datos

            # Verificar si se realizaron las inserciones
            resultado = cursor.rowcount > 0
            cursor.close()
            return resultado
        except Exception as e:
            print(f"Error al registrar el libro: {e}")
            return False

    @classmethod
    def modificar_libro(cls, db, isbn, titulo, apellidos, nombres, precio, descripcion, portada):
        try:
            cursor = db.connection.cursor()

            # Llamada al procedimiento almacenado para modificar el libro
            cursor.execute('SET SQL_SAFE_UPDATES = 0;')  # Desactivar actualizaciones seguras
            cursor.execute('CALL modificar_libro(%s, %s, %s, %s, %s, %s, %s)',
                           (isbn, titulo,apellidos,  nombres, precio, descripcion, portada))


            db.connection.commit()  # Confirmar los cambios en la base de datos

            # Verificar si se realizaron las modificaciones
            resultado = cursor.rowcount > 0
            cursor.close()
            return resultado
        except Exception as e:
            print(f"Error al modificar el libro: {e}")
            return False

    @classmethod
    def eliminar_libro(self, db, isbn):
        try:
            cursor = db.connection.cursor()
            print("MODELO LIBRO  " + isbn)

            # Llamada al procedimiento almacenado
            cursor.execute('CALL EliminarLibro(%s)', (isbn,))

            # Consumir todos los conjuntos de resultados
            while cursor.nextset():
                pass

            # Confirmar cambios
            db.connection.commit()

            # Opcional: verificar algún estado devuelto
            resultado = cursor.fetchone()
            if resultado and resultado[0] == 1:  # Suponiendo que devuelve un indicador de éxito
                cursor.close()
                return True
            else:
                cursor.close()
                return False

        except Exception as e:
            print(f"Error al eliminar el libro: {e}")
            return False