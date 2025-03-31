from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import Usuario, db  # Importar el modelo desde models.py
from sqlalchemy import func

# Crear la aplicación Flask
app = Flask(__name__)

# Cargar la configuración desde el archivo config.py
app.config.from_object(Config)

# Instanciar SQLAlchemy
#db = SQLAlchemy(app)
db.init_app(app)

# Crear la base de datos si no existe
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('ingreso.html')

@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    # Obtener los datos del formulario
    usuario = request.form['usuario']
    nombre = request.form['nombre']
    cedula = request.form['cedula']
    contrasena = request.form['contrasena']
    fecha_registro = db.Column(db.DateTime, nullable=False, default=func.now())

    # Crear una nueva instancia del modelo Estudiante
    nuevo_usuario = Usuario(cedula=cedula, nombre=nombre, usuario=usuario, contrasena=contrasena, fechaRegistro=fecha_registro)

    # Agregar el estudiante a la base de datos
    db.session.add(nuevo_usuario)
    db.session.commit()

    return render_template('ingreso.html')

    #return redirect('/')

@app.route('/ingresar')
def inicio():
    return render_template('ingreso.html')

@app.route('/registro-usuario')
def registro_usuario():
    return render_template('registro_usuario.html')

@app.route('/iniciar-sesion', methods=['POST'])
def inicioSesion():

    usuario = request.form['usuario']
    contrasena = request.form['contrasena']

    # Verificar usuario y contraseña
    usuario_encontrado = Usuario.query.filter_by(usuario=usuario, contrasena=contrasena).first()

    if usuario_encontrado:
        return render_template('dashboard.html', usuario=usuario_encontrado)
    else:
        print("usuario incorrecto")
        return redirect('/ingresar')

@app.route('/registrar-cuenta')
def registrar_cuenta():
    return render_template('registrar_cuenta.html')

@app.route('/salir')
def salir():
    return redirect('/ingresar')




if __name__ == '__main__':
    app.run(debug=True)