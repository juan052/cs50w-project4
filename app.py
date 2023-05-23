import os
import datetime
import requests
import uuid
from flask import Flask, session, redirect, url_for, render_template, request, flash,jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from models import *
from sqlalchemy.orm import joinedload
app = Flask(__name__)

# Check for environment variable
# Set up database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SESSION_PERMANENT"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = 'static/img/imagenes'
Session(app)
db.init_app(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db_session = scoped_session(sessionmaker(bind=engine))
# Subir foto al servidor
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return filename
    else:
        return 'No se proporcionó ningún archivo'
    

# Inicio
@app.route("/")
def index():
    return render_template('inicio.html')



@app.route("/categoria")
def categoria():
    categorias = CategoriaProducto.query.all()
    return render_template('categoria.html', categorias=categorias)

@app.route("/crear_categoria", methods=["GET", "POST"])
def crear_categoria():
    if request.method == "POST":
        nombre = request.form.get('nombre')
        descripcion= request.form.get('descripcion')
        estado = request.form.get('estado')
        categoria = CategoriaProducto(nombre=nombre, descripcion=descripcion, estado=estado)
        db.session.add(categoria)
        db.session.commit()
        return redirect(url_for('categoria'))
    else:
        return render_template('categoria.html')
    
@app.route("/editar_categoria/<int:id>", methods=["GET", "POST"])
def editar_categoria(id):
    categoria = CategoriaProducto.query.get(id)
    if request.method == "POST":
        categoria.nombre = request.form.get('nombre')
        categoria.descripcion = request.form.get('descripcion')
        categoria.estado = request.form.get('estado')
        db.session.commit()
        return redirect(url_for('categoria'))
    else:
       return redirect(url_for('categoria'))
    
@app.route("/eliminar_categoria", methods=["POST"])
def eliminar_categoria():
    categoria_id = request.form.get("id")
    categoria = CategoriaProducto.query.get(categoria_id)

    if categoria:
        # Cambiar el estado de la categoría a inactivo (estado = 2)
        categoria.estado = 2
        db.session.commit()

    return redirect(url_for('categoria'))

@app.route("/sub")
def sub():
    categorias = CategoriaProducto.query.all()
    subcategorias = SubCategoriaProducto.query.options(joinedload(SubCategoriaProducto.categoria)).all()
    return render_template('sub_categoria.html', categorias=categorias, subcategorias=subcategorias)

@app.route("/crear_sub", methods=["GET", "POST"])
def crear_sub():
   
    if request.method == "POST":
        categoria=request.form.get('categoria')
        nombre = request.form.get('nombre')
        descripcion= request.form.get('descripcion')
        estado = request.form.get('estado')
        sub = SubCategoriaProducto(id_categoria=categoria,nombre=nombre, descripcion=descripcion, estado=estado)
        db.session.add(sub)
        db.session.commit()
        
        return redirect(url_for('sub'))
    else:
        return render_template('sub_categoria.html')
    

@app.route("/sub_actualizar/<int:id>", methods=["GET", "POST"])
def sub_actualizar(id):
    sub = SubCategoriaProducto.query.get(id)
    if request.method == "POST":
        sub.id_categoria = request.form.get('categoria')
        sub.nombre = request.form.get('nombre')
        sub.descripcion = request.form.get('descripcion')
        sub.estado = request.form.get('estado')
        db.session.commit()
        return redirect(url_for('sub'))
    else:
        return render_template('sub_categoria.html')


@app.route("/eliminar_sub", methods=["POST"])
def eliminar_sub():
    sub_id = request.form.get("id")
    subcategoria = SubCategoriaProducto.query.get(sub_id)

    if subcategoria:
        # Cambiar el estado de la categoría a inactivo (estado = 2)
        subcategoria.estado = 2
        db.session.commit()

    return redirect(url_for('sub'))


@app.route("/producto", methods=["GET", "POST"])
def producto():
    
    producto = Producto.query.options(joinedload(Producto.subcategoria).joinedload(SubCategoriaProducto.categoria)).all()
    subcategorias = SubCategoriaProducto.query.options(joinedload(SubCategoriaProducto.categoria)).all()
    return render_template("producto.html", producto=producto,subcategorias=subcategorias)


@app.route("/producto_crear", methods=["GET","POST"])
def producto_crear():
    if request.method == "POST":
        id_sub_categoria=request.form.get('subcategoria')
        nombre = request.form.get('nombre')
        descripcion= request.form.get('descripcion')
        cantidad=request.form.get('cantidad')
        estado = request.form.get('estado')
        logo = None
        if 'foto' in request.files:
            logo = request.files['foto']
            print(logo)
            if logo:
                filename = str(uuid.uuid4()) + secure_filename(logo.filename)
                logo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                logo = filename
        print(logo)
        producto=Producto(id_sub_categoria=id_sub_categoria, nombre=nombre, descripcion=descripcion, cantidad=cantidad,logo=logo, estado=estado)
        db.session.add(producto)
        db.session.commit()
        return redirect(url_for('producto'))
    else:
        return redirect(url_for('producto'))
    

@app.route("/producto_actualizar/<int:producto_id>", methods=["GET", "POST"])
def producto_actualizar(producto_id):
    producto = Producto.query.get_or_404(producto_id)

    if request.method == "POST":
        id_sub_categoria = request.form.get('subcategoria')
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        cantidad = request.form.get('cantidad')
        estado = request.form.get('estado')
        logo = producto.logo

        if 'foto' in request.files:
            nueva_logo = request.files['foto']
            if nueva_logo:
                # Eliminar la imagen anterior si existe
                if logo:
                    eliminar_logo_antigua(logo)
                
                # Guardar la nueva imagen
                filename = str(uuid.uuid4()) + secure_filename(nueva_logo.filename)
                nueva_logo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                logo = filename

        producto.id_sub_categoria = id_sub_categoria
        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.cantidad = cantidad
        producto.logo = logo
        producto.estado = estado

        db.session.commit()
        return redirect(url_for('producto'))
    else:
        return redirect(url_for('producto'))

@app.route("/eliminar_producto", methods=["POST"])
def eliminar_producto():
    producto_id = request.form.get("id")
    print(producto_id)
    productos = Producto.query.get(producto_id)
    
    if productos:
        # Cambiar el estado de la categoría a inactivo (estado = 2)
        productos.estado = 2
        db.session.commit()

    return redirect(url_for('producto'))


def eliminar_logo_antigua(filename):
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(path):
        os.remove(path)


@app.route("/precio_producto",methods=["POST","GET"])
def precio_producto():
   Precios=Precio.query.options(joinedload(Precio.producto)).all()
   productos = Producto.query.options(joinedload(Producto.subcategoria).joinedload(SubCategoriaProducto.categoria)).all()

   return render_template("precio_producto.html",Precios=Precios,productos=productos)



@app.route("/crear_precio",methods=["GET","POST"])
def crear_precio():
    if request.method == "POST":
        id_producto=request.form.get('producto')
        precio_actual = request.form.get('precio_actual')
        estado=request.form.get('estado')
        precio = Precio(id_producto=id_producto, precio_actual=precio_actual, precio_anterior=0, estado=estado)
        db.session.add(precio)
        db.session.commit()

        return redirect(url_for('precio_producto'))
    else:
        return redirect(url_for('precio_producto'))
    


@app.route("/actualizar_precio/<int:id>",methods=["GET","POST"])
def actualizar_precio(id):
    precio = Precio.query.get(id)
    if request.method == "POST":
        
        precio_actual = request.form.get('precio_actual')
        precio_anterior=request.form.get('precio_anterior')
        estado=request.form.get('estado')
       
      
        precio.precio_actual=precio_actual
        precio.precio_anterior=precio_anterior
        precio.estado=estado
        db.session.commit()
        return redirect(url_for('precio_producto'))
    else:
        return redirect(url_for('precio_Producto'))