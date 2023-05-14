import os
import datetime
import requests
from flask import Flask, session, redirect, url_for, render_template, request, flash,jsonify
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from flask_session import Session
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)

# Check for environment variable
# Set up database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SESSION_PERMANENT"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['UPLOAD_FOLDER'] = 'static/img/user'
Session(app)
db.init_app(app)

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# Inicio
@app.route("/")
def index():
 

    return render_template('inicio.html')

@app.route("/producto")
def producto():
    return render_template('producto.html')

@app.route("/categoria")
def categoria():
  

  return render_template('categoria.html')

@app.route("/crear_categoria", methods=["GET", "POST"])
def crear_categoria():
    if request.method == "POST":
        nombre = request.form.get('nombre')
        descripcion= request.form.get('descripcion')
        estado = request.form.get('estado')
        print(nombre)
        print(descripcion)
        print(estado)
        categoria = CategoriaProducto(nombre=nombre, descripcion=descripcion, estado=estado)
        db.session.add(categoria)
        db.session.commit()
        return redirect(url_for('categoria'))
    else:
        return render_template('categoria.html')


@app.route("/sub")
def sub():

    return render_template('sub_categoria.html')
