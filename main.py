from flask import Flask,render_template,request, flash, g, redirect, url_for, session
from flask_wtf.csrf import CSRFProtect
import forms, csv
from config import DevelopmentConfig
from sqlalchemy import extract, func

from datetime import datetime

from models import db
from models import Empleados, Ventas

app=Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/index',methods=['GET', 'POST'])
def index():
     create_form = forms.UserForm(request.form)
     if request.method == 'POST':
          emp = Empleados(nombre = create_form.nombre.data,
                          direccion = create_form.direccion.data,
                          telefono = create_form.telefono.data,
                          correo = create_form.correo.data,
                          sueldo = create_form.sueldo.data)
          db.session.add(emp)
          db.session.commit()
     return render_template('index.html', form = create_form)
 
@app.route('/eliminar',methods=['GET', 'POST'])
def eliminar():
    create_form = forms.UserForm(request.form)
    if request.method == 'GET':
         id = request.args.get('id')
         emp1 = db.session.query(Empleados).filter(Empleados.id == id).first()
         create_form.id.data = request.args.get('id') #id = request.args.get('id')
         create_form.nombre.data = emp1.nombre
         create_form.direccion.data = emp1.direccion
         create_form.telefono.data = emp1.telefono
         create_form.correo.data = emp1.correo
         create_form.sueldo.data = emp1.sueldo
    if request.method == 'POST':
         id = create_form.id.data
         emp = Empleados.query.get(id)
         db.session.delete(emp)
         db.session.commit()
         return redirect(url_for('ABCompleto'))
    return render_template('eliminar.html', form=create_form)

@app.route('/modificar',methods=['GET', 'POST'])
def modificar():
    create_form = forms.UserForm(request.form)
    if request.method == 'GET':
         id = request.args.get('id')
         emp1 = db.session.query(Empleados).filter(Empleados.id == id).first()
         create_form.id.data = request.args.get('id') #id = request.args.get('id')
         create_form.nombre.data = emp1.nombre
         create_form.direccion.data = emp1.direccion
         create_form.telefono.data = emp1.telefono
         create_form.correo.data = emp1.correo
         create_form.sueldo.data = emp1.sueldo
    if request.method == 'POST':
         id = create_form.id.data
         emp1 = db.session.query(Empleados).filter(Empleados.id == id).first()
         emp1.nombre = create_form.nombre.data
         emp1.direccion = create_form.direccion.data
         emp1.telefono = create_form.telefono.data
         emp1.correo = create_form.correo.data
         emp1.sueldo = create_form.sueldo.data
         #emp = Empleados.query.get(id)
         db.session.add(emp1)
         db.session.commit()
         return redirect(url_for('ABCompleto'))
    return render_template('modificar.html', form=create_form)

ventas_registradas = []

@app.route("/pizzas", methods=['GET', 'POST'])
def venderPizzas():
     precio_tamanio = 0.0
     precio_ingredientes = 0.0
     pizzas_form = forms.VentasForm(request.form)
     precio_total = 0.0
     venta = None
     pizzas = 0
     filtromes = None
     filtrodia = None
     filtro_dia = None
     filtro_mes = None
     if request.method == 'POST':
          
          #variable para filtrar las ventas
          filtro_ventas = Ventas.query
          
          ingredientes_seleccionados = ', '.join(pizzas_form.ingredientes_pizza.data)
          cantidad_comas = ingredientes_seleccionados.count(', ')

          if ingredientes_seleccionados == '':#precio_ingredientes = 10
               precio_ingredientes = 0.0
          else:
               if cantidad_comas == 0:
                    precio_ingredientes = 10
               elif cantidad_comas == 1:
                    precio_ingredientes = 20
               elif cantidad_comas == 2:
                    precio_ingredientes = 30
               
          tamanio = pizzas_form.tamanio_pizza.data
          
          if tamanio == 'Chica':
               precio_tamanio = 40
          elif tamanio == 'Mediana':
               precio_tamanio = 80
          elif tamanio == 'Grande':
               precio_tamanio = 120
               
          pizzas = pizzas_form.cantidad_pizzas.data        
          
          if precio_tamanio is not None and precio_ingredientes is not None and pizzas is float:
               precio_total = 0.0
          else:
               precio_total = (precio_tamanio + precio_ingredientes) * pizzas
               
          print(precio_total, precio_tamanio, precio_ingredientes, pizzas)
          
          texto_nombre_completo = pizzas_form.nombre_completo.data
          texto_direccion = pizzas_form.direccion.data
          texto_telefono = pizzas_form.telefono.data
          texto_fecha_compra = pizzas_form.fecha_compra.data
          texto_tamanio_pizza = pizzas_form.tamanio_pizza.data
          texto_ingredientes_pizza = ingredientes_seleccionados
          texto_cantidad_pizzas = str(pizzas)
          texto_total_venta = precio_total
               
          if 'btn1' in request.form:
               archivo1 = open('archivo.txt', 'a') #Abrimos el archivo en modo lectura
               venta_temporal = '\n' + texto_nombre_completo + ';' + texto_direccion + ';' + texto_telefono + ';' + str(texto_fecha_compra) + ';' + str(texto_tamanio_pizza) + ';' + texto_ingredientes_pizza + ';' + texto_cantidad_pizzas + ';' + str(texto_total_venta)
               print(venta_temporal)
               archivo1.write(venta_temporal)  #Escribimos la venta temporal en el archivo
               archivo1.close()  #Cerramos el archivo

               ventas_registradas.clear()  #Limpiar el arreglo antes de agregar nuevas ventas

               #Leer y agregar solo la nueva venta al arreglo
               with open('archivo.txt', 'r') as archivo_lectura:
                    lineas = archivo_lectura.readlines()  #Lee todas las líneas del archivo y las guarda en una lista

               for linea in lineas:
                    #Dividir la venta con un ';'
                    elementos = linea.strip().split(';')

                    #Guardarlos en una lista
                    ventas_registradas.append(elementos)

               print(ventas_registradas)

          elif 'btn2' in request.form:
               if ventas_registradas:
                    for venta in ventas_registradas:
                         if len(venta) >= 8:
                              nueva_venta = Ventas(
                                   nombre_completo=venta[0],
                                   direccion=venta[1],
                                   telefono=venta[2],
                                   fecha_compra=venta[3],
                                   tamanio_pizza=venta[4],
                                   ingredientes_pizza=venta[5],
                                   cantidad_pizzas=int(venta[6]),
                                   total_venta=float(venta[7])
                              )
                              db.session.add(nueva_venta)
                    db.session.commit()
                    ventas_registradas.clear()
                    flash('Venta de pizzas registrada correctamente', 'success')
               else:
                    flash('No hay ventas registradas para procesar', 'warning')
               
               with open('archivo.txt', 'w') as archivo:
                    archivo.write('')
                    
          elif 'btn3' in request.form:
               # Obtener los valores seleccionados del filtro de día y mes
               
               #filtro_dia = request.form.get('filtro_dia')
               #filtro_mes = request.form.get('filtro_mes')               

               if request.form.get("filtro_dia") == None :
                    filtro_dia = ""
               else: 
                    filtro_dia = request.form.get("filtro_dia").lower()
                    
               if request.form.get("filtro_mes") == None :
                    filtro_mes = ""
               else: 
                    filtro_mes = request.form.get("filtro_mes").lower()

               print("Filtro día:", filtro_dia)
               print("Filtro mes:", filtro_mes)

               fechas = {"":0, "domingo":1, "lunes":2, "martes":3, "miercoles":4, "jueves":5, "viernes":6, "sabado":7}
               meses = {"":0, "enero":1,"febrero":2,"marzo":3,"abril":4,"mayo":5,"junio":6,"julio":7,"agosto":8,"septiembre":9,"octubre":10,"noviembre":11,"diciembre":12}

               filtrodia = Ventas.query.filter(func.dayofweek(Ventas.fecha_compra) == fechas.get(filtro_dia ,0)).all()

               filtromes = Ventas.query.filter(extract('month', func.date(Ventas.fecha_compra)) == meses.get(filtro_mes , 0)).all()
          
          elif 'btn4' in request.form:
               # Obtener el índice del botón en el formulario
               indice_eliminar = int(request.form['btn4'])
               
               # Eliminar la venta del arreglo ventas_registradas
               venta_eliminada = ventas_registradas.pop(indice_eliminar - 1)  # Restamos 1 porque los índices en Python comienzan desde 0
               
               # Actualizar el archivo.txt con las ventas restantes
               with open('archivo.txt', 'w') as archivo:
                    for venta in ventas_registradas:
                         venta_temporal = ';'.join(venta)
                         archivo.write(venta_temporal + '\n')

               # Mensaje de éxito
               flash(f'Venta de {venta_eliminada[0]} eliminada correctamente', 'success')
     
     venta = Ventas.query.all()
     
     totalventas = Ventas.query.with_entities(func.sum(Ventas.total_venta)).scalar() or 0
     totalventasdia = sum(venta.total_venta for venta in filtrodia) if filtrodia else 0
     totalventasmes = sum(venta.total_venta for venta in filtromes) if filtromes else 0
     
     #print(venta)
     return render_template("pizzas.html", form=pizzas_form, 
                                             ventas_registradas = ventas_registradas,
                                             filtrodia = filtrodia,
                                             filtromes = filtromes,
                                             totalventas = totalventas,
                                             totalventasdia = totalventasdia,
                                             totalventasmes = totalventasmes,
                                             venta = venta)

@app.route("/empleado_tabla", methods=["GET", "POST"])
def ABCompleto():
    emp_form = forms.UserForm(request.form)
    empleado = Empleados.query.all()
    
    return render_template("empleado_tabla.html", empleado = empleado)

if __name__=="__main__":
    csrf.init_app(app)    
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
    app.run()
    