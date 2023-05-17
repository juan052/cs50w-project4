from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
db = SQLAlchemy()

class CategoriaProducto(db.Model):
    __tablename__ = 'categoria_producto'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.String(250))
    estado = db.Column(db.Integer)
    
    def __init__(self, nombre, descripcion, estado):
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado

    

class SubCategoriaProducto(db.Model):
    __tablename__ = 'sub_categoria_producto'

    id = db.Column(db.Integer, primary_key=True)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria_producto.id'))
    nombre = db.Column(db.String(250), nullable=False)
    descripcion = db.Column(db.String(250))
    estado = db.Column(db.Integer)
    categoria = relationship('CategoriaProducto')
    
    def __init__(self, id_categoria, nombre, descripcion, estado):
        self.id_categoria = id_categoria
        self.nombre = nombre
        self.descripcion = descripcion
        self.estado = estado

class Producto(db.Model):
    __tablename__ = 'producto'

    id = db.Column(db.Integer, primary_key=True)
    id_sub_categoria = db.Column(db.Integer, db.ForeignKey('sub_categoria_producto.id'))
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.String(250), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    logo=db.Column(db.String(250), nullable=False)
    estado = db.Column(db.Integer)
    subcategoria = relationship('SubCategoriaProducto')
    
    def __init__(self, id_sub_categoria, nombre, descripcion, cantidad,logo, estado):
        self.id_sub_categoria = id_sub_categoria
        self.nombre = nombre
        self.descripcion = descripcion
        self.cantidad = cantidad
        self.logo=logo
        self.estado = estado

class Precio(db.Model):
    __tablename__ = 'precio'

    id = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'))
    precio_actual = db.Column(db.Numeric(10,2), nullable=False)
    precio_anterior = db.Column(db.Numeric(10,2), nullable=False)
    estado = db.Column(db.Integer)
    producto = relationship('Producto')
    
    def __init__(self,id_producto,precio_actual,precio_anterior,estado):
        self.id_producto=id_producto
        self.precio_actual=precio_actual
        self.precio_anterior=precio_anterior
        self.estado=estado




class Persona(db.Model):
    __tablename__='persona'
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Colum(db.String(120),nullable=False)
    correo=db.Colum(db.String(250),nullable=False)
    direccion=db.Colum(db.String(250),nullable=True)
    celular=db.Colum(db.Integer)

    def __init__(self,nombre,correo,direccion,celular):
        self.nombre=nombre
        self.correo=correo
        self.direccion=direccion
        self.celular=celular


class PersonaNatural(db.Model):
    __table__='persona_natural'
    id=db.Column(db.Integer,primary_key=True)
    id_persona=db.Column(db.Integer, db.ForeignKey('persona.id'))
    apellido=db.Column(db.String(250),nullable=False)
    cedula=db.Colum(db.String(80),nullable=False)
    fecha_nacmiento=db.Colum(db.Date,nullable=False)
    genero=db.Colum(db.String,nullable=True)


