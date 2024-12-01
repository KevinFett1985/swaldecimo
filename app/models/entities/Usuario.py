from werkzeug.security import generate_password_hash, check_password_hash #validar contraseñas
from flask_login import UserMixin

 
class Usuario(UserMixin):
    
    def __init__(self, id, usuario, password=None, tipousuario=None, direccion=None, telefono=None, email=None):
        self.id = id
        self.usuario = usuario
        self.password = password
        self.tipousuario = tipousuario
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
            
    @classmethod
    def verificar_password(self,encriptado,password):
        #encriptado=generate_password_hash(password)
        #coincide=check_password_hash(encriptado,password) #Haciendo la comparación del la pass con ell encriptado
        #return 'Encriptado: {0} | Coincide: {1}'.format(encriptado, coincide)
        return check_password_hash(encriptado,password)
        """
                  @classmethod
        def crear(cls, id, usuario, password, tipousuario,direccion,telefono,email):
            c=cls.__new__(cls)
            c.id=id,
            c.usuario = usuario
            c.password = password
            c.tipousuario = tipousuario     
            c.direccion=direccion
            c.email=email
            c.telefono= telefono
     
            """
  
     
class newUsuario():
    def __init__(self, id, usuario, password, tipousuario,direccion,telefono,email):
        self.id=id,
        self.usuario = usuario
        self.password = password
        self.tipousuario = tipousuario     
        self.direccion=direccion
        self.telefono= telefono
        self.email=email
    
    @classmethod
    def verificar_password(self,encriptado,password):
         return check_password_hash(encriptado, password)