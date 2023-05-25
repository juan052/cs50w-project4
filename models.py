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
    __tablename__ = 'persona'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    correo = db.Column(db.String(150), nullable=False)
    direccion = db.Column(db.String(250), nullable=False)
    celular = db.Column(db.Integer)
    persona_natural = db.relationship('PersonaNatural', uselist=False)
    def __init__(self, nombre, correo, direccion, celular=None):
        self.nombre = nombre
        self.correo = correo
        self.direccion = direccion
        self.celular = celular


class PersonaNatural(db.Model):
    __tablename__ = 'persona_natural'

    id = db.Column(db.Integer, primary_key=True)
    id_persona = db.Column(db.Integer, db.ForeignKey('persona.id'))
    apellido = db.Column(db.String(250), nullable=False)
    cedula = db.Column(db.String(80))
    fecha_nacimiento = db.Column(db.Date)
    genero = db.Column(db.CHAR)
    persona = relationship('Persona', back_populates='persona_natural')

    def __init__(self, id_persona, apellido, cedula, fecha_nacimiento, genero):
        self.id_persona = id_persona
        self.apellido = apellido
        self.cedula = cedula
        self.fecha_nacimiento = fecha_nacimiento
        self.genero = genero


class PersonaJuridica(db.Model):
    __tablename__ = 'persona_juridica'

    id = db.Column(db.Integer, primary_key=True)
    id_persona = db.Column(db.Integer, db.ForeignKey('persona.id'))
    ruc = db.Column(db.String(250), nullable=False)
    razon_social = db.Column(db.String(250))
    fecha_constitucional = db.Column(db.Date)
    persona = relationship('Persona')



class Clientes(db.Model):
    __tablename__ = 'clientes'

    id = db.Column(db.Integer, primary_key=True)
    id_persona = db.Column(db.Integer, db.ForeignKey('persona.id'))
    tipo_cliente = db.Column(db.String(250), nullable=False)
    foto = db.Column(db.String(250))
    estado = db.Column(db.Integer)
    persona = relationship('Persona')

    def __init__(self, id_persona, tipo_cliente, foto=None, estado=None):
        self.id_persona = id_persona
        self.tipo_cliente = tipo_cliente
        self.foto = foto
        self.estado = estado


class Trabajador(db.Model):
    __tablename__ = 'trabajador'

    id = db.Column(db.Integer, primary_key=True)
    id_persona = db.Column(db.Integer, db.ForeignKey('persona.id'))
    foto = db.Column(db.String(250))
    estado = db.Column(db.Integer)
    persona = relationship('Persona')
    def __init__(self,id_persona,foto,estado):
        self.id_persona=id_persona
        self.foto=foto
        self.estado=estado

class Salario(db.Model):
    __tablename__ = 'salario'

    id = db.Column(db.Integer, primary_key=True)
    id_trabajador = db.Column(db.Integer, db.ForeignKey('trabajador.id'))
    salario_actual = db.Column(db.Numeric(10,2), nullable=False)
    salario_anterior = db.Column(db.Numeric(10,2))
    estado = db.Column(db.Integer)



