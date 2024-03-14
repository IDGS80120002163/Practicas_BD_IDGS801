from wtforms import Form, StringField, EmailField, IntegerField, FloatField, DateField, RadioField, SelectMultipleField
# Aquí de los validadores importamos el dato obligatorio y el email
from wtforms import validators#, DataRequired, Email}
    
class VentasForm(Form):
    
    opciones_ingredientes = [('Jamon', 'Jamon'), ('Pina', 'Pina'), ('Champinon', 'Champinon')]
    
    opciones_tamanios = [('Chica', 'Chica'), ('Mediana', 'Mediana'), ('Grande', 'Grande')]    
    
    id = IntegerField('id', [
        validators.number_range(min=1, max=20, message='Valor no válido')
    ])   
    nombre_completo = StringField('nombre_completo', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=50, message='Ingresa un nombre válido')
    ])
    direccion = StringField('direccion', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=50, message='Ingresa un apellido válido')
    ])
    telefono = StringField('telefono', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=4, max=50, message='Ingresa un número de teléfono válido')
    ])
    fecha_compra = DateField('fecha_compra', [
        validators.DataRequired(message='El campo es requerido')
    ])
    tamanio_pizza = RadioField("tamanio_pizza", choices=opciones_tamanios, validators=[
        validators.DataRequired(message='El campo es requerido')
    ])
    ingredientes_pizza = SelectMultipleField("ingredientes_pizza", choices=opciones_ingredientes, validators=[
        validators.DataRequired(message='El campo es requerido')
    ])
    cantidad_pizzas = IntegerField("cantidad_pizzas", [
        validators.Length(min =1, message = 'Mínimo 1 pizza'),
        validators.DataRequired(message='El campo es requerido')
    ])

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
