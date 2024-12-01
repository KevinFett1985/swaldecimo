class Autor():
    
    def __init__(self, id, apellidos, nombres, fechadenacimiento=None ):
        self.id=id
        self.apellidos=apellidos
        self.nombres=nombres
        self.fechadenacimiento=fechadenacimiento
        
    def nombre_completo(self):
        return "{0},{1}".format( self.apellidos,self.nombres)