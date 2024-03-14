from flask_sqlalchemy import SQLAlchemy

import datetime

db = SQLAlchemy()

class Empleados(db.Model):
    __tablename__ = 'empleados'
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(50))
    direccion = db.Column(db.String(50))
    telefono = db.Column(db.String(50))
    correo = db.Column(db.String(50))
    sueldo = db.Column(db.Float)
    
class Ventas(db.Model):
    __tablename__ = 'ventas'
    id = db.Column(db.Integer, primary_key = True)
    nombre_completo = db.Column(db.String(50))
    direccion = db.Column(db.String(50))
    telefono = db.Column(db.String(50))
    fecha_compra = db.Column(db.Date)
    tamanio_pizza = db.Column(db.String(50))
    ingredientes_pizza = db.Column(db.String(50))
    cantidad_pizzas = db.Column(db.Integer)
    total_venta = db.Column(db.Float)
    