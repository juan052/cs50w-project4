import os
from datetime import datetime
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
from helper import *
from helper1 import *
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
    usuario = session.get('cliente_id')
    if usuario is None:
        # La sesión no existe
        # Realiza alguna acción o redirige a otra página
        Precios = Precio.query.options(joinedload(Precio.producto)).limit(4).all()
        return render_template('index.html', Precios=Precios)
    else:
        # La sesión existe
        Precios = Precio.query.options(joinedload(Precio.producto)).limit(4).all()
        return render_template('index.html', Precios=Precios, usuario=usuario)

@app.route("/home")
def home():
    usuario = session.get('cliente_id')
    if usuario is None:
        # La sesión no existe
        # Realiza alguna acción o redirige a otra página
        Precios = Precio.query.options(joinedload(Precio.producto)).limit(4).all()
        return render_template('index.html', Precios=Precios)
    else:
        # La sesión existe
        Precios = Precio.query.options(joinedload(Precio.producto)).limit(4).all()
        return render_template('index.html', Precios=Precios, usuario=usuario)
@app.route("/logout")
def logout():
      # Borrar toda la sesión
    session.clear()

    # Redireccionar al inicio de sesión
    return redirect(url_for('home'))

@app.route("/acerca")
def acerca():
    usuario = session.get('cliente_id')
    if usuario is None:
        # La sesión no existe
        # Realiza alguna acción o redirige a otra página
        return render_template('about.html')
    else:
        # La sesión existe
        
        return render_template('about.html', usuario=usuario)

@app.route("/shop")
def shop():
    usuario = session.get('cliente_id')
    if usuario is None:
        # La sesión no existe
        # Realiza alguna acción o redirige a otra página
        Precios = Precio.query.options(joinedload(Precio.producto)).all()
        return render_template('index.html', Precios=Precios)
    else:
        # La sesión existe
        Precios=Precio.query.options(joinedload(Precio.producto)).all()
        return render_template('shop.html', Precios=Precios,usuario=usuario)
    
   

@app.route("/inicio")
@login_required
def inicio():
    usuario = session.get('trabajador_id')
    return render_template('inicio.html',usuario=usuario)


@app.route("/categoria")
@login_required
def categoria():
    categorias = CategoriaProducto.query.all()
    return render_template('categoria.html', categorias=categorias)

@app.route("/crear_categoria", methods=["GET", "POST"])
@login_required
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
@login_required
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
@login_required
def eliminar_categoria():
    categoria_id = request.form.get("id")
    categoria = CategoriaProducto.query.get(categoria_id)

    if categoria:
        # Cambiar el estado de la categoría a inactivo (estado = 2)
        categoria.estado = 2
        db.session.commit()

    return redirect(url_for('categoria'))

@app.route("/sub")
@login_required
def sub():
    categorias = CategoriaProducto.query.all()
    subcategorias = SubCategoriaProducto.query.options(joinedload(SubCategoriaProducto.categoria)).all()
    return render_template('sub_categoria.html', categorias=categorias, subcategorias=subcategorias)

@app.route("/crear_sub", methods=["GET", "POST"])
@login_required
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
@login_required
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
@login_required
def eliminar_sub():
    sub_id = request.form.get("id")
    subcategoria = SubCategoriaProducto.query.get(sub_id)

    if subcategoria:
        # Cambiar el estado de la categoría a inactivo (estado = 2)
        subcategoria.estado = 2
        db.session.commit()

    return redirect(url_for('sub'))


@app.route("/producto", methods=["GET", "POST"])
@login_required
def producto():
    
    producto = Producto.query.options(joinedload(Producto.subcategoria).joinedload(SubCategoriaProducto.categoria)).all()
    subcategorias = SubCategoriaProducto.query.options(joinedload(SubCategoriaProducto.categoria)).all()
    return render_template("producto.html", producto=producto,subcategorias=subcategorias)


@app.route("/producto_crear", methods=["GET","POST"])
@login_required
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
@login_required
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
@login_required
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
@login_required
def precio_producto():
   Precios=Precio.query.options(joinedload(Precio.producto)).all()
   productos = Producto.query.options(joinedload(Producto.subcategoria).joinedload(SubCategoriaProducto.categoria)).all()

   return render_template("precio_producto.html",Precios=Precios,productos=productos)



@app.route("/crear_precio",methods=["GET","POST"])
@login_required
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
@login_required
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

@app.route("/trabajador",methods=["GET","POST"])
@login_required
def trabajador():
    trabajadores = Trabajador.query.options(joinedload(Trabajador.persona)).all()
    return render_template("trabajador.html", trabajadores=trabajadores) 


@app.route("/crear_trabajador",methods=["GET","POST"])
@login_required
def crear_trabajador():
    if request.method == "POST":
        nombre=request.form.get('nombre')
        apellido = request.form.get('apellido')
        cedula=request.form.get('cedula')
        fecha=request.form.get('fecha_nacimiento')
        correo=request.form.get('correo')
        direccion=request.form.get('direccion')
        genero=request.form.get('genero')
        celular=request.form.get('celular')
        estado=request.form.get('estado')
        logo = None
        if 'foto' in request.files:
            logo = request.files['foto']
            print(logo)
            if logo:
                filename = str(uuid.uuid4()) + secure_filename(logo.filename)
                logo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                logo = filename
        print(logo)
        persona=Persona(nombre=nombre,correo=correo,direccion=direccion,celular=celular)
        db.session.add(persona)
        db.session.commit()
        id_persona=persona.id
        personanat=PersonaNatural(id_persona=id_persona,apellido=apellido,cedula=cedula,fecha_nacimiento=fecha,genero=genero)
        db.session.add(personanat)
        db.session.commit()
        colaborador=Trabajador(id_persona=id_persona,foto=logo,estado=estado)
        db.session.add(colaborador)
        db.session.commit()
        return redirect(url_for('trabajador'))
    else:
        return redirect(url_for('trabajador')) 






#Usuarios
@app.route("/usuarios",methods=["GET","POST"])
@login_required
def usuarios():
    trabajadores = Trabajador.query.join(Persona).all()
    return render_template("usuarios.html", trabajadores=trabajadores)

@app.route("/crear_usuarios",methods=["GET","POST"])
@login_required
def crear_usuarios():
    if request.method == "POST":
        persona=request.form.get('id_persona')
        correo = request.form.get('correo')
        contraseña=request.form.get('contraseña')
        hashed_password = generate_password_hash(contraseña)
        usuario = Usuario(id_grupo=1, id_persona=persona, usuario=correo, contraseña=hashed_password, estado=1)
        db.session.add(usuario)
        db.session.commit()
        return redirect("usuarios")
    return render_template("usuarios.html")

@app.route("/login",methods=["GET","POST"])
def login():
 
    return render_template("login.html")



@app.route("/validar", methods=["GET", "POST"])
def validar():
    if request.method == "POST":
        usuario = request.form.get('usuario')
        contraseña = request.form.get('contraseña')

        # Obtener el usuario de la base de datos por nombre de usuario
        usuario_db = Usuario.query.filter_by(usuario=usuario).first()

        if usuario_db and check_password_hash(usuario_db.contraseña, contraseña):
            # Las contraseñas coinciden, el usuario es válido
            if usuario_db.id_grupo == 2:
                
                cliente = Cliente.query.filter_by(id_persona=usuario_db.id_persona).first()
                persona = Persona.query.filter_by(id=usuario_db.id_persona).first()
                session['cliente_id'] = cliente.id
                session['cliente_foto'] = cliente.foto
                session['cliente_nombre'] = persona.nombre
                session['cliente_direccion'] = persona.direccion
                session['cliente_celular'] = persona.celular
                session['cliente_correo']=persona.correo
                return redirect(url_for('home'))
            elif usuario_db.id_grupo == 1:
                 print("Entró en el bloque elif")
                 print("usuario_db.id_grupo:", usuario_db.id_grupo)
                 trabajador = Trabajador.query.filter_by(id_persona=usuario_db.id_persona).first()
                 print("trabajador:", trabajador)
                 persona = Persona.query.filter_by(id=usuario_db.id_persona).first()
                 print("persona:", persona)
                 session['user_id'] = trabajador.id
                 session['trabajador_foto'] = trabajador.foto
                 session['trabajador_nombre'] = persona.nombre
                 session['trabajador_direccion'] = persona.direccion
                 session['trabajador_celular'] = persona.celular
                 print("Antes de la redirección a 'inicio'")
                 return redirect(url_for('producto'))
            
        else:
            flash("Usuario y/o contraseña incorrectos. Acceso denegado.", "error")
            print("no entre")
            return redirect(url_for('login'))
    else:
        return render_template("login.html")


def obtener_productos():
    productos = Producto.query.all()
    lista_productos = []
    
    for producto in productos:
        precio = Precio.query.filter_by(id_producto=producto.id).first()
        precio_actual = precio.precio_actual if precio else None
        lista_productos.append({
            'id': producto.id,
            'nombre': producto.nombre,
            'precio': precio_actual,
            'logo': producto.logo
        })
    
    return lista_productos



@app.route('/agregar', methods=['POST'])
def agregar():
    carrito = session.get('carrito', [])
    
    for key, value in request.form.items():
        print("Clave:", key)
        print("Valor:", value)
        if key.startswith('producto_id_'):
            producto_id = int(key.split('_')[2])  # Obtener el ID del producto del nombre de la clave
            cantidad_key = 'cantidad_' + str(producto_id)  # Construir la clave específica de cantidad
            cantidad = int(request.form.get(cantidad_key, 1))
            
            for item in carrito:
                if item['id'] == producto_id:
                    item['cantidad'] += cantidad
                    break
            else:
                producto = {'id': producto_id, 'cantidad': cantidad}
                carrito.append(producto)
                break  # Agrega el producto y sale del bucle principal
    print("Carrito actualizado:", carrito)
    session['carrito'] = carrito
    return redirect('/shop')





# Ruta para mostrar el carrito
@app.route("/card", methods=["GET", "POST"])
@login_requirede
def card():
    carrito = session.get('carrito', [])
    productos = obtener_productos()

    carrito_actualizado = []
    for item in carrito:
        for producto in productos:
            if producto['id'] == item['id']:
                item_actualizado = {
                    'id': item['id'],
                    'nombre': producto['nombre'],
                    'precio': producto['precio'],
                    'logo': producto['logo'],
                    'cantidad': item['cantidad'] 
                }
                carrito_actualizado.append(item_actualizado)
                break

     # Guardar los detalles de la venta en la sesión
    session['detalles_venta'] = carrito_actualizado
    return render_template("card.html", carrito=carrito_actualizado)



# Ruta para eliminar productos del carrito
@app.route('/eliminar/<int:producto_id>')
def eliminar(producto_id):
    carrito = session.get('carrito', [])
    
    # Buscamos el producto en el carrito y lo eliminamos
    for item in carrito:
        if item['id'] == producto_id:
            carrito.remove(item)
            break
    
    # Actualizamos el carrito en la sesión
    session['carrito'] = carrito
    
    return redirect('/card')

@app.route('/registro')
def registro():
   
 
    return render_template("registro_usuario.html")




@app.route('/registrase', methods=["GET", "POST"])
def registrase():
    if request.method == "POST":
        # Obtener los datos del formulario
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        telefono = request.form.get("telefono")
        fecha_nacimiento_str = request.form.get("fecha")
        cedula = request.form.get("cedula")
        genero = request.form.get("genero")
        email = request.form.get("email")
        contraseña = request.form.get("contraseña")
        direccion = request.form.get("Direccion")
        logo = None
        if 'foto' in request.files:
            logo = request.files['foto']
            if logo:
                filename = str(uuid.uuid4()) + secure_filename(logo.filename)
                logo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                logo = filename
        
        fecha_nacimiento = datetime.datetime.strptime(fecha_nacimiento_str, "%Y-%m-%d").date()
        usuario_existente = Usuario.query.filter_by(usuario=email).first()
        if usuario_existente:
            # El email ya está registrado, mostrar mensaje de error
            flash("El email ya está registrado", "error")
            return redirect('/registrase')

        # Crear una instancia de Persona y PersonaNatural
        persona = Persona(nombre=nombre, correo=email, direccion=direccion, celular=telefono)
        persona_natural = PersonaNatural(id_persona=persona.id, apellido=apellido, cedula=cedula, fecha_nacimiento=fecha_nacimiento, genero=genero)

        # Asociar Persona y PersonaNatural
        persona.persona_natural = persona_natural

        # Realizar las acciones necesarias para guardar los modelos en la base de datos
        db.session.add(persona)
        db.session.commit()

        # Generar el hash de la contraseña
        hashed_password = generate_password_hash(contraseña)
        usuario = Usuario(id_grupo=2, id_persona=persona.id, usuario=email, contraseña=hashed_password, estado=1)
        persona.usuario = usuario

        # Crear una instancia de Cliente y asociarla a Persona
        cliente = Cliente(id_persona=persona.id, tipo_cliente="Normal", foto=logo, estado=1)
        persona.cliente = cliente

        # Agregar los objetos a la sesión de la base de datos y confirmar los cambios
        db.session.add(usuario)
        db.session.add(cliente)
        db.session.commit()

        # Redirigir al usuario a la página de inicio de sesión después del registro exitoso
        return redirect('/login')

    return render_template('registro_usuario.html')



@app.route('/guardar_venta', methods=['POST'])
def guardar_venta():
    # Obtener los datos de la venta desde la solicitud
    id_tipo = request.form.get('id_tipo')
    id_cliente = session['cliente_id']
    fecha = request.form.get('fecha')
    estado = request.form.get('estado')
    fecha_actual = datetime.now()

    # Formatear la fecha en formato PostgreSQL
    fecha_postgresql = fecha_actual.strftime('%Y-%m-%d')
    # Crear una instancia de Venta
    venta = Venta(id_tipo=1, id_cliente=id_cliente, fecha=fecha_postgresql, estado=1)
    db.session.add(venta)

    db.session.commit()

    # Obtener los detalles de la venta desde la solicitud
    # Obtener los detalles de la venta desde la sesión
    detalles = session.get('detalles_venta', [])

    # Crear instancias de DetalleVenta y asociarlas a la venta
    for detalle in detalles:
        id_producto = detalle['id']
        subtotal = detalle['precio'] * detalle['cantidad']
        descuento = 0
        total = subtotal - descuento
        detalle_venta = DetalleVenta(id_venta=venta.id, id_producto=id_producto, subtotal=subtotal, descuento=descuento, total=total)
        db.session.add(detalle_venta)
    
    db.session.commit()
      # Eliminar el carrito de la sesión
    session.pop('carrito', None)
    return redirect('/shop')
    


@app.route('/ventas', methods=['GET'])
@login_required
def ventas():
    # Obtener todos los registros de los modelos
    ventas = Venta.query\
    .options(joinedload(Venta.tipo_venta), joinedload(Venta.cliente).joinedload(Cliente.persona))\
    .all()

# Pasar los datos a la plantilla
    return render_template('venta.html', ventas=ventas)
