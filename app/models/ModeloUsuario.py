#from werkzeug.security import generate_password_hash, check_password_hash #validar contraseñas
from .entities.Usuario import Usuario, newUsuario 
from .entities.TipoUsuario import TipoUsuario 

class ModeloUsuario():
    
    @classmethod
    def login(self, db, usuario):
        try:
            cursor = db.connection.cursor()
            sql="""SELECT id, usuario, password FROM 
            usuario WHERE usuario = '{0}'""".format(usuario.usuario)
            cursor.execute(sql)
            data=cursor.fetchone()
            print(data)
            #coincide=check_password_hash(data[2],usuario.password) #validacion de la contraseña del login contra la bd
            if data!=None:
                coincide=Usuario.verificar_password(data[2],usuario.password)
                if coincide:
                    usuario_logeado=Usuario(data[0],data[1],None,None)
                    return usuario_logeado
                else:
                    return None
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def Obtener_por_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT USU.id, USU.usuario, TIP.id, TIP.nombre, USU.direccion, USU.telefono, USU.email
                     FROM usuario USU JOIN tipousuario TIP ON USU.tipousuario_id = TIP.id
                     WHERE USU.id = {0}""".format(id)
            cursor.execute(sql)
            data = cursor.fetchone()
            print(data)
            if data:
                tipousuario = TipoUsuario(data[2], data[3])
                usuario_logeado = Usuario(data[0], data[1], tipousuario=tipousuario, direccion=data[4], telefono=data[5], email=data[6])
                return usuario_logeado
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
   
    #agregada primero
    def registrar_cliente(self, db, usuario):
        try:
            cursor = db.connection.cursor()
            print(usuario.usuario)
            print(usuario.password)
            print(usuario.direccion)
            print(usuario.telefono)
            print(usuario.email)
            sql = """insert into usuario (usuario,password,tipousuario_id,direccion,telefono,email) 
                    values ('{0}','{1}',2,'{2}','{3}','{4}')""".format(usuario.usuario, usuario.password, usuario.direccion, usuario.telefono, usuario.email)
            cursor.execute(sql)
            db.connection.commit()  # Confirmar la transacción
            if cursor.rowcount > 0:  # Verificar si se insertó al menos una fila
                return True 
            else:
                return False  # Devolver False si la operación no fue exitosa
        except Exception as ex:
            db.connection.rollback()  # Revertir la transacción en caso de error
            raise Exception(ex)