from wtforms import Form, StringField, EmailField, IntegerField, FloatField
# Aquí de los validadores importamos el dato obligatorio y el email
from wtforms import validators#, DataRequired, Email}
    
class UserForm(Form):
    id=IntegerField('id',[
        validators.number_range(min=1, max=20, message='valor no valido')
    ])   
    nombre = StringField('nombre', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=50, message='Ingresa un nombre válido')
    ])
    direccion = StringField('direccion', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=50, message='Ingresa un apellido válido')
    ])
    telefono = StringField('telefono', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=7, max=13, message='Ingresa un número de teléfono válido')
    ])
    correo = EmailField('correo', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Email(message='Ingresa un email válido')
    ])
    sueldo=FloatField('sueldo',[
        validators.number_range(min=1, max=5000, message='valor no valido')
    ])  
