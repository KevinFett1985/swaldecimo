import datetime
from contextlib import nullcontext


class Compra():
    
    def __init__(self,uuid, libro,usuario,fecha=None,portada=None):
        self.uuid=uuid
        self.libro=libro
        self.usuario=usuario
        self.fecha=fecha
        self.portada=portada
        
    def formatted_date(self):
        return datetime.datetime.strftime(self.fecha,'%d/%m/%Y - %H:%M:%S ' )