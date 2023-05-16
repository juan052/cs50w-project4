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
    estado = db.Column(db.Integer)

class Precio(db.Model):
    __tablename__ = 'precio'

    id = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer, db.ForeignKey('producto.id'))
    precio_actual = db.Column(db.Numeric(10,2), nullable=False)
    precio_anterior = db.Column(db.Numeric(10,2), nullable=False)
    estado = db.Column(db.Integer)
