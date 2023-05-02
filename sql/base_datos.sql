CREATE TABLE persona (
 id SERIAL PRIMARY KEY,
 nombre VARCHAR(150) NOT NULL,
 correo VARCHAR(150) NOT NULL,
 direccion VARCHAR(250) NOT NULL,
 celular INTEGER
);
CREATE TABLE persona_natural (
    id SERIAL PRIMARY KEY,
    id_persona INTEGER REFERENCES persona(id),
    apellido VARCHAR(250) NOT NULL,
    cedula VARCHAR(80),
    fecha_nacimiento DATE,
    genero CHAR
);

CREATE TABLE persona_juridica
(
    id SERIAL PRIMARY KEY,
    id_persona INTEGER REFERENCES persona(id),
    ruc VARCHAR(250) NOT NULL,
    razon_social VARCHAR(250),
    fecha_constitucional DATE
);

CREATE TABLE clientes (
    id SERIAL PRIMARY KEY,
    id_persona INTEGER REFERENCES persona(id),
    tipo_cliente VARCHAR(250) NOT NULL,
    foto VARCHAR(250) ,
    estado INTEGER
);
CREATE TABLE estado_civil
(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion VARCHAR(250)
);

CREATE TABLE trabajador
(
    id SERIAL primary key,
    id_persona INTEGER REFERENCES persona(id),
    id_estado_civil INTEGER REFERENCES estado_civil(id),
    foto VARCHAR(250) ,
    estado INTEGER 
);


CREATE TABLE salario
( 
    id SERIAL PRIMARY KEY,
    id_trabajador INTEGER REFERENCES trabajador(id),
    salario_actual NUMERIC(10,2) NOT NULL,
    salario_anterior NUMERIC(10,2)
    fecha_cambio DATE,
    estado INTEGER
);
/*ESTA PARTE ES PARA AYUDAR A CONTROLAR EL INVENTARIO*/
CREATE TABLE categoria_producto
(
    id SERIAL PRIMARY KEY ,
    nombre VARCHAR(120) NOT NULL,
    descripcion VARCHAR(250),
    estado INTEGER
);

CREATE TABLE sub_categoria_producto(
    id SERIAL PRIMARY KEY,
    id_categoria INTEGER REFERENCES categoria(id),
    nombre VARCHAR(250) NOT NUll,
    descripcion VARCHAR(250),
    estado INTEGER
);

CREATE TABLE marca
(
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL
    descripcion VARCHAR(250),
    estado INTEGER
);


CREATE TABLE unidad_medida (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NUll,
    descripcion VARCHAR(250),
    estado INTEGER
);

CREATE TABLE producto
(
    id SERIAL PRIMARY KEY,
    id_sub_categoria INTEGER REFERENCES sub_categoria_producto(id),
    id_marca INTEGER REFERENCES marca(id),
    id_unidad_medida INTEGER REFERENCES unidad_medida(id),
    nombre VARCHAR(120) NOT NULL,
    descripcion varchar(250) NOT NULL,
    cantidad INTEGER NOT NUll,
    estado INTEGER
);

CREATE TABLE precio(
    id SERIAL PRIMARY KEY
);
