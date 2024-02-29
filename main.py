from flask import Flask,render_template,request, flash, g
from flask_wtf.csrf import CSRFProtect
import forms
from config import DevelopmentConfig

from models import db
from models import Empleados

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
    