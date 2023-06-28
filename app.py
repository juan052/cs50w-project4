import os
from datetime import datetime
import random
import string
import requests
import uuid
from flask import Flask, session, redirect, url_for, render_template, request, flash,jsonify
from werkzeug.utils import secure_filename
from flask_mail import Mail, Message
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
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'ingsoftwar123@gmail.com'
app.config['MAIL_PASSWORD'] = 'uwyzadkpqxkxzhvr'
app.secret_key = 'tu_clave_secreta'
mail = Mail(app)
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
        if precio_actual and precio_actual.strip():  
            precio.precio_actual=precio_actual
            precio.precio_anterior=precio_anterior
            precio.estado=estado
            db.session.commit()
            return redirect(url_for('precio_producto'))
        else:
            precio.estado=estado
            db.session.commit()
            return redirect(url_for('precio_producto'))
      
        
    else:
        return redirect(url_for('precio_Producto'))

@app.route("/eliminar_precio", methods=["POST"])
@login_required
def eliminar_precio():
    id = request.form.get("id")
    
    productos = Precio.query.get(id)
    
    if productos:
        # Cambiar el estado de la categoría a inactivo (estado = 2)
        productos.estado = 2
        db.session.commit()

    return redirect(url_for('precio_producto'))

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


@app.route("/actualizar_trabajador/<int:id>", methods=["GET", "POST"])
@login_required
def actualizar_trabajador(id):
    trabajador = Trabajador.query.get_or_404(id)
    persona = Persona.query.get_or_404(trabajador.id_persona)
    personanat = PersonaNatural.query.get_or_404(trabajador.id_persona)

    if request.method == "POST":
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        cedula = request.form.get('cedula')
        fecha = request.form.get('fecha_nacimiento')
        correo = request.form.get('correo')
        direccion = request.form.get('direccion')
        genero = request.form.get('genero')
        celular = request.form.get('celular')
        estado = request.form.get('estado')
        logo = trabajador.foto
         
        if 'foto' in request.files:
            archivo_foto = request.files['foto']
            if archivo_foto:
                # Eliminar el archivo de foto actual si existe
                if logo:
                    eliminar_logo_antigua(logo)

                # Guardar el nuevo archivo de foto
                filename = str(uuid.uuid4()) + secure_filename(archivo_foto.filename)
                archivo_foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                logo = filename

        persona.nombre = nombre
        persona.correo = correo
        persona.direccion = direccion
        persona.celular = celular

        personanat.apellido = apellido
        personanat.cedula = cedula
        personanat.fecha_nacimiento = fecha
        personanat.genero = genero

        trabajador.foto = logo
        trabajador.estado = estado

        db.session.commit()

        return redirect(url_for('trabajador'))
    else:
        return render_template('trabajador.html', trabajador=trabajador, persona=persona, personanat=personanat)

@app.route("/eliminar_trabajador",methods=["GET","POST"])
def eliminar_colaborador():
    if request.method == "POST":
        id=request.form.get('id')
        trabajador=Trabajador.query.get(id)
        if trabajador:
        # Cambiar el estado de la categoría a inactivo (estado = 2)
            trabajador.estado = 2
            db.session.commit()

        usuario=Usuario.query.filter_by(id_persona=trabajador.id_persona).first()
        if usuario:
        # Cambiar el estado de la categoría a inactivo (estado = 2)
            usuario.estado = 2
            db.session.commit()

        return redirect(url_for('trabajador'))
    
    
    
    return redirect(url_for('trabajador'))


#Usuarios
@app.route("/usuarios",methods=["GET","POST"])
@login_required
def usuarios():
    trabajadores = Trabajador.query.join(Persona).all()
    usuarios=Usuario.query.filter_by(id_grupo=1).all()
    return render_template("usuarios.html", trabajadores=trabajadores,usuarios=usuarios)


def generar_contraseña():
    caracteres = string.ascii_letters + string.digits  # Letras mayúsculas, minúsculas y dígitos
    longitud = 8
    contraseña = ''.join(random.choice(caracteres) for _ in range(longitud))
    return contraseña


@app.route("/crear_usuarios",methods=["GET","POST"])
@login_required
def crear_usuarios():
    if request.method == "POST":
        persona=request.form.get('id_persona')
        correo = request.form.get('correo')
        contraseña=generar_contraseña()
        cuerpo = '''
    Estimado(a) ,

    Aquí tienes la contraseña para acceder a tu cuenta:

    Contraseña: {0}

    Por favor, asegúrate de cambiar tu contraseña una vez que hayas iniciado sesión en tu cuenta.

    Si tienes alguna pregunta o necesitas asistencia adicional, no dudes en contactarnos.

    ¡Gracias y ten un excelente día!

    Atentamente, Luxx ART
    '''.format(contraseña)
        msg = Message('Asignacion de contraseña - Acceso a cuenta', sender='ingsoftwar123@gmail.com', recipients=[correo])
        msg.body = cuerpo
        mail.send(msg)
        hashed_password = generate_password_hash(contraseña)
        usuario = Usuario(id_grupo=1, id_persona=persona, usuario=correo, contraseña=hashed_password, estado=0)
        db.session.add(usuario)
        db.session.commit()
        return redirect("usuarios")
    return render_template("usuarios.html")

@app.route("/verificar_usuarios",methods=["GET","POST"])
def verificar():
    if request.method == "POST":
        id=request.form.get('id')
        usuario=Usuario.query.get(id)
        trabajador=Trabajador.query.filter_by(id_persona=usuario.id_persona).first()
        if trabajador.estado == 2:
            flash("No se puede activar el usuario, el trabajador es inactivo","Error")
            return  redirect(url_for('usuarios'))
        
        else:
            if usuario:
            # Cambiar el estado de la categoría a inactivo (estado = 2)
                usuario.estado = 1
                db.session.commit()

                return redirect(url_for('usuarios'))
    
    
    
    return redirect(url_for('usuarios'))

@app.route("/eliminar_usuario",methods=["GET","POST"])
def eliminar_usuario():
    if request.method == "POST":
        id=request.form.get('id')
        usuario=Usuario.query.get(id)
        if usuario:
        # Cambiar el estado de la categoría a inactivo (estado = 2)
            usuario.estado = 2
            db.session.commit()

        return redirect(url_for('usuarios'))
    
    
    
    return redirect(url_for('usuarios'))

@app.route("/cambiar_contraseña",methods=["GET","POST"])
@login_required
def cambiar_contraseña():
    if request.method == "POST":
        id=request.form.get('id')
        usuario=Usuario.query.get(id)
        print(usuario)
        contraseña_anterior=request.form.get('contraseña_actual')
        contraseña_nueva =request.form.get('contraseña_nueva')
        confirmacion=request.form.get('confirmacion')
        usuario = Usuario.query.get(id)
        if usuario is None:
         # Manejar el caso cuando el usuario no existe
            return "El usuario no existe"

  
        if not check_password_hash(usuario.contraseña, contraseña_anterior):
        # Manejar el caso cuando la contraseña actual no coincide
            flash("La contraseña actual no coincide", "error")
            return redirect(url_for('admin'))
    
        if contraseña_nueva != confirmacion:
            # Manejar el caso cuando la confirmación de contraseña no coincide
            flash("La contraseña nueva no coinciden.", "error")
            return redirect(url_for('admin'))
        
        hashed_password = generate_password_hash(contraseña_nueva)
        usuario.contraseña=hashed_password
        db.session.commit()
        flash("Se ha cambiado la contraseña correctamente", "Exito")
        return redirect(url_for('admin'))

    
    return redirect(url_for('admin'))

@app.route("/recuperar_contraseña",methods=["GET","POST"])
def recuperar_contraseña():
    if request.method == "POST":
        correos=request.form.get('correo')
        usuario=Usuario.query.filter_by(usuario=correos).first()
        print(usuario)
       
        if usuario is None:
         # Manejar el caso cuando el usuario no existe
             flash("Se ha enviando un codigo de verificacion al correo", "error")
             return redirect(url_for('recuperar_contraseña'))
        contraseña=generar_contraseña()
        cuerpo = '''
    Estimado(a) ,
    Aquí está tu código de seguridad para acceder al cambio de contraseña:   codigo de verficiacion: {0}
    Por favor, utiliza este código al realizar el cambio de contraseña en tu cuenta. Si tienes alguna pregunta o necesitas asistencia adicional, no dudes en contactarnos.
    ¡Gracias y ten un excelente día!

    Atentamente, Luxx ART
    '''.format(contraseña)
        msg = Message('Codigo de verificacion - Acceso a cuenta', sender='ingsoftwar123@gmail.com', recipients=[correos])
        msg.body = cuerpo
        mail.send(msg)
        hashed_password = generate_password_hash(contraseña)
        usuario.contraseña=hashed_password
        db.session.commit()
        flash("Se ha enviando un codigo de verificacion al correo", "success")
        return render_template("verficar_contraseña.html",correo=correos)


    
    return render_template("recuperar_contraseña.html")

@app.route("/nueva_contraseña", methods=["GET", "POST"])
def nueva_contraseña():
    
    if request.method == "POST":
        correos=request.form.get('correo')
        print("Coreo----------------------")
        print(correos)
        print("Correo--------------")
        usuario = Usuario.query.filter_by(usuario=correos).first()
        print(usuario)
        contraseña_anterior = request.form.get('codigo_verficacion')
        contraseña_nueva = request.form.get('contraseña_nueva')
        confirmacion = request.form.get('confirmacion')
        print(contraseña_nueva)
        print(confirmacion)
        if usuario is None:
            # Manejar el caso cuando el usuario no existe
            flash("El código no coincide, revisa tu correo nuevamente", "error")
            return render_template("verficar_contraseña.html",correo=correos)

        if not check_password_hash(usuario.contraseña, contraseña_anterior):
            # Manejar el caso cuando la contraseña actual no coincide
            flash("El código no coincide, revisa tu correo nuevamente", "error")
            return render_template("verficar_contraseña.html",correo=correos)

        if contraseña_nueva != confirmacion:
            # Manejar el caso cuando la confirmación de contraseña no coincide
            flash("La contraseña nueva no coincide", "error")
            return render_template("verficar_contraseña.html",correo=correos)

        hashed_password = generate_password_hash(contraseña_nueva)
        usuario.contraseña = hashed_password
        db.session.commit()
        flash("Se ha cambiado la contraseña correctamente", "success")
        return redirect(url_for('login'))

    return render_template("verficar_contraseña.html")





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
            elif usuario_db.id_grupo == 1 and usuario_db.estado == 1 :
                
                 trabajador = Trabajador.query.filter_by(id_persona=usuario_db.id_persona).first()
                 print("trabajador:", trabajador)
                 persona = Persona.query.filter_by(id=usuario_db.id_persona).first()
                 print("persona:", persona)
                 session['user_id'] = trabajador.id
                 session['trabajador_foto'] = trabajador.foto
                 session['trabajador_nombre'] = persona.nombre
                 session['trabajador_direccion'] = persona.direccion
                 session['trabajador_celular'] = persona.celular
                 session['id_usuario']=usuario_db.id
                 return redirect(url_for('admin'))
            else:
                flash("Acceso denegado.", "error")
                return  redirect(url_for('login'))
        else:
            flash("Usuario y/o contraseña incorrectos. Acceso denegado.", "error")
           
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
        fecha_nacimiento = request.form.get("fecha")
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



@app.route('/admin',methods=["GET"])
@login_required
def admin():
    # Obtener la fecha y hora actual
    now = datetime.now()

    # Obtener la hora actual
    hora_actual = now.hour
    minutos_actuales = now.minute

    # Determinar si es de mañana, tarde o noche
    if hora_actual >= 6 and hora_actual < 12:
        momento = "mañana"
    elif hora_actual >= 12 and hora_actual < 18:
        momento = "tarde"
    else:
        momento = "noche"

    # Obtener la fecha actual
    fecha_actual = now.strftime("%d/%m/%Y")

    return render_template("inicio_admin.html", hora_actual=hora_actual,minutos_actuales=minutos_actuales,momento=momento,fecha_actual=fecha_actual)


@app.route('/servicios', methods=['POST','GET'])
@login_required
def servicios():
    servicios= Servicio.query.all()
    return render_template("servicios.html",servicios=servicios)

@app.route('/crear_servicios', methods=['POST','GET'])
def crear_servicios():
    nombre = request.form.get('nombre')
    descripcion = request.form.get('descripcion')
    logo = None
    if 'foto' in request.files:
        logo = request.files['foto']
        if logo:
            filename = str(uuid.uuid4()) + secure_filename(logo.filename)
            logo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            logo = filename
    estado = request.form.get('estado')

    servicio = Servicio(nombre=nombre, descripcion=descripcion, foto=logo, estado=estado)
    db.session.add(servicio)
    db.session.commit()

    return redirect('servicios')

@app.route('/actualizar_servicios/<int:servicio_id>', methods=['POST','GET'])
def actualizar_servicio(servicio_id):
    servicio = Servicio.query.get(servicio_id)

    if servicio:
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        estado = request.form.get('estado')
        logo=servicio.foto
        print(logo)
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

        servicio.nombre = nombre
        servicio.descripcion = descripcion
        servicio.estado = estado
        servicio.foto=logo
        db.session.commit()

        return redirect('/servicios')
    else:
        return jsonify({'error': 'No se encontró el servicio'})


@app.route('/eliminar_servicio/<int:servicio_id>', methods=['POST','GET'])
def eliminar_servicio(servicio_id):
    servicio = Servicio.query.get(servicio_id)

    if servicio:
        servicio.estado = 2
        db.session.commit()

        return redirect("/servicios")
    else:
        return jsonify({'error': 'No se encontró el servicio'})


@app.route("/precio_servicios",methods=["POST","GET"])
@login_required
def precio_servicios():
   Precios=PrecioServicio.query.options(joinedload(PrecioServicio.servicio)).all()
   servicio=Servicio.query.all()
   return render_template("precio_servicios.html",Precios=Precios,servicio=servicio)

@app.route("/crear_precio_servicio",methods=["GET","POST"])
@login_required
def crear_precio_servicio():
    if request.method == "POST":
        id_producto=request.form.get('producto')
        precio_actual = request.form.get('precio_actual')
        estado=request.form.get('estado')
        precio = PrecioServicio(id_servicios=id_producto, precio_actual=precio_actual, precio_anterior=0, estado=estado)
        db.session.add(precio)
        db.session.commit()

        return redirect(url_for('precio_servicios'))
    else:
        return redirect(url_for('precio_servicios'))
    


@app.route("/actualizar_precio_servicio/<int:id>",methods=["GET","POST"])
@login_required
def actualizar_precio_servicio(id):
    precio = PrecioServicio.query.get(id)
    if request.method == "POST":
        
        precio_actual = request.form.get('precio_actual')
        precio_anterior=request.form.get('precio_anterior')
        estado=request.form.get('estado')
        if precio_actual and precio_actual.strip():  
            precio.precio_actual=precio_actual
            precio.precio_anterior=precio_anterior
            precio.estado=estado
            db.session.commit()
            return redirect(url_for('precio_servicios'))
        else:
            precio.estado=estado
            db.session.commit()
            return redirect(url_for('precio_servicios'))
        
    else:
        return redirect(url_for('/precio_servicios'))

@app.route("/eliminar_precio_servicio", methods=["POST"])
@login_required
def eliminar_precio_servicio():
    id = request.form.get("id")
    
    productos = PrecioServicio.query.get(id)
    
    if productos:
        # Cambiar el estado de la categoría a inactivo (estado = 2)
        productos.estado = 2
        db.session.commit()

    return redirect(url_for('precio_servicios'))

#Clientes
@app.route("/clientes",methods=["POST","GET"])
@login_required
def cliente():
    clientes=Cliente.query.options(joinedload(Cliente.persona)).all()
    return render_template("cliente.html",clientes=clientes)


@app.route('/crear_cliente', methods=["GET", "POST"])
@login_required
def crear_cliente():
    if request.method == "POST":
        # Obtener los datos del formulario
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        telefono = request.form.get("celular")
        fecha_nacimiento = request.form.get("fecha")
        cedula = request.form.get("cedula")
        genero = request.form.get("genero")
        email = request.form.get("email")
        tipo=request.form.get("tipo")
        direccion = request.form.get("direccion")
        logo = None
        if 'foto' in request.files:
            logo = request.files['foto']
            if logo:
                filename = str(uuid.uuid4()) + secure_filename(logo.filename)
                logo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                logo = filename
        
        
     

        # Crear una instancia de Persona y PersonaNatural
        persona = Persona(nombre=nombre, correo=email, direccion=direccion, celular=telefono)
        persona_natural = PersonaNatural(id_persona=persona.id, apellido=apellido, cedula=cedula, fecha_nacimiento=fecha_nacimiento, genero=genero)

        # Asociar Persona y PersonaNatural
        persona.persona_natural = persona_natural

        # Realizar las acciones necesarias para guardar los modelos en la base de datos
        db.session.add(persona)
        db.session.commit()

      
        # Crear una instancia de Cliente y asociarla a Persona
        cliente = Cliente(id_persona=persona.id, tipo_cliente=tipo, foto=logo, estado=1)
        persona.cliente = cliente

        # Agregar los objetos a la sesión de la base de datos y confirmar los cambios
       
        db.session.add(cliente)
        db.session.commit()

        # Redirigir al usuario a la página de inicio de sesión después del registro exitoso
        return redirect('/clientes')

    return render_template('cliente.html')


@app.route('/actualizar_cliente/<int:id>', methods=["GET", "POST"])
@login_required
def actualizar_cliente(id):
   
    cliente = Cliente.query.get(id)
    print(cliente)
    if request.method == "POST":
        # Obtener los datos del formulario
        nombre = request.form.get("nombre")
        apellido = request.form.get("apellido")
        telefono = request.form.get("celular")
        fecha_nacimiento = request.form.get("fecha_nacimiento")
        cedula = request.form.get("cedula")
        genero = request.form.get("genero")
        email = request.form.get("correo")
        tipo = request.form.get("tipo")
        direccion = request.form.get("direccion")
        estado=request.form.get("estado")
        logo = cliente.foto
        if 'foto' in request.files:
            archivo_foto = request.files['foto']
            if archivo_foto:
                # Eliminar el archivo de foto actual si existe
                if logo:
                    eliminar_logo_antigua(logo)

                # Guardar el nuevo archivo de foto
                filename = str(uuid.uuid4()) + secure_filename(archivo_foto.filename)
                archivo_foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                logo = filename

       
        # Actualizar los datos del cliente existente
        cliente.persona.nombre = nombre
        cliente.persona.correo = email
        cliente.persona.direccion = direccion
        cliente.persona.celular = telefono
        cliente.persona.persona_natural.apellido = apellido
        cliente.persona.persona_natural.cedula = cedula
        cliente.persona.persona_natural.fecha_nacimiento = fecha_nacimiento
        cliente.persona.persona_natural.genero = genero
        cliente.tipo_cliente = tipo
        cliente.foto = logo
        cliente.estado=estado
        db.session.add(cliente)
        db.session.commit()
        print("--------Estado aqui abajo de esta linea")
        print(estado)
        print("---------------------------------------------------")
        if int(estado) == 1:
            usuario=Usuario.query.filter_by(id_persona=cliente.id_persona).first()
            print(cliente.id_persona)
            print("-----------------------------------------------------")
            print(usuario)
            print("---------------------------------------------------------")
            if usuario:
            # Cambiar el estado de la categoría a inactivo (estado = 2)
                usuario.estado = 1
                print("Se cambio estado")
                db.session.commit()

        return redirect('/clientes')

    return redirect('/clientes')


@app.route("/eliminar_cliente",methods=["GET","POST"])
def eliminar_cliente():
    if request.method == "POST":
        id=request.form.get('id')
        trabajador=Cliente.query.get(id)
        if trabajador:
        # Cambiar el estado de la categoría a inactivo (estado = 2)
            trabajador.estado = 2
            db.session.commit()

        usuario=Usuario.query.filter_by(id_persona=trabajador.id_persona).first()
        if usuario:
        # Cambiar el estado de la categoría a inactivo (estado = 2)
            usuario.estado = 2
            db.session.commit()

        return redirect('/clientes')
    
    
    
    return redirect('/clientes')