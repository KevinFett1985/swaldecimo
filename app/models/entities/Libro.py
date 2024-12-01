class Libro():
    
    def __init__(self, isbn, titulo, autor, portada,precio):
        self.isbn=isbn 
        self.titulo=titulo
        self.autor=autor
        self.portada=portada
        self.precio=precio
        self.unidades_vendidas=0

class newLibro():
    def __init__(self,titulo, isbn, precio, nombre, apellido, descripcion,portada):
        self.isbn=isbn
        self.titulo=titulo
        self.nombre=nombre
        self.precio=precio
        self.apellido=apellido
        self.descripcion=descripcion
        self.portada=portada