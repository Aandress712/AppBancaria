from flask import Flask, render_template, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
from config import Config
from models import Usuario, db  # Importar el modelo desde models.py
from models import Cuenta
from models import Transaccion
from sqlalchemy import func
from decimal import Decimal
from random import randint, random
from fpdf import FPDF
import io

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
    activa = db.Column(db.Boolean, default=True)
    intentos = db.Column(db.Integer, default=0)

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

    global inicioUsuario
    intentos =0

    # Verificar usuario y contraseña
    usuario_encontrado = Usuario.query.filter_by(usuario=usuario).first()
    inicioUsuario = usuario_encontrado

    if usuario_encontrado:
        if not usuario_encontrado.activa:
            # Si el usuario está desactivado
            print("Usuario desactivado, contacte al administrador")
            return redirect('/ingresar')

        if usuario_encontrado.contrasena == contrasena:
            # Restablecer intentos si el inicio de sesión es correcto
            usuario_encontrado.intentos = 0
            db.session.commit()
            inicioUsuario = usuario_encontrado
            return render_template('dashboard.html', usuario=usuario_encontrado)
        
        else:
            # Incrementar intentos fallidos
            usuario_encontrado.intentos += 1
            if usuario_encontrado.intentos >= 3:
                # Desactivar usuario después de 3 intentos fallidos
                usuario_encontrado.activa = False
                print("Usuario desactivado después de 3 intentos fallidos")
            db.session.commit()
    
    print("Usuario o contraseña incorrectos")
    return redirect('/ingresar')

@app.route('/registrar-cuenta')
def registro_cuenta():
    
    numero_cuenta = str(randint(300, 999)) + "-" + str(inicioUsuario.cedula) + "-" + str(randint(1000, 9999))
    print(numero_cuenta)
    return render_template('registrar_cuenta.html', usuario=inicioUsuario, numero_cuenta=numero_cuenta)

@app.route('/crear_cuenta', methods=['POST'])
def crear_cuenta():
    cedula_usuario = inicioUsuario.cedula
    numero_cuenta = request.form['numero_cuenta']
    tipo_cuenta = request.form['tipo_cuenta']
    saldo = request.form['saldo']
    cedula = cedula_usuario
    fecha_registro = db.Column(db.DateTime, nullable=False, default=func.now())

    # Crear una nueva instancia del modelo Cuenta
    nueva_cuenta = Cuenta(numeroCuenta=numero_cuenta, tipoCuenta=tipo_cuenta, saldo=saldo, cedula=cedula, fechaRegistroCuenta=fecha_registro)

    # Agregar la cuenta a la base de datos
    db.session.add(nueva_cuenta)
    db.session.commit()

    # Redirigir a un dashboard o página de confirmación
    return render_template('dashboard.html', usuario=inicioUsuario)

@app.route('/retiro')
def retiro():
    
    usuario_id=inicioUsuario.cedula
    cuentas_origen = Cuenta.query.filter_by(cedula=usuario_id).first()
    return render_template('retiro.html', usuario=inicioUsuario , cuenta=cuentas_origen)

@app.route('/retirar', methods=['POST'])
def retirar():

    usuario_id=inicioUsuario.cedula
    cuentas_origen = Cuenta.query.filter_by(cedula=usuario_id).first()
    retiro= request.form['valor']
    valorRetiro= Decimal(retiro)

    if cuentas_origen.saldo<valorRetiro:
        print("No tienes saldo disponible")
    else:
        cuentas_origen.saldo = cuentas_origen.saldo-valorRetiro
        db.session.commit()

    return render_template('dashboard.html', usuario=inicioUsuario)

@app.route('/transaccion')
def transferencia():

    usuario_id=inicioUsuario.cedula
    cuentas_origen = Cuenta.query.filter_by(cedula=usuario_id).all()
    cuentas_inscritas = Cuenta.query.all()
    cuentasActual = cuentas_origen
    return render_template('transferencia.html', cuentas_origen=cuentas_origen, cuentas_inscritas=cuentas_inscritas, usuario=inicioUsuario)

@app.route('/transferir', methods=['POST'])
def realizarTransferencia():

    cuentaOrigen = request.form['cuenta_origen']
    cuentaDestino = request.form['cuenta_destino']
    monto = request.form['valor']
    cedulaUsuario = inicioUsuario.cedula
    valorTransferencia= Decimal(monto)

    cuentasOrigen = Cuenta.query.filter_by(numeroCuenta=cuentaOrigen).first()
    cuentasDestino = Cuenta.query.filter_by(numeroCuenta=cuentaDestino).first()

    nuevaTransaccion= Transaccion(cuentaOrigen=cuentaOrigen, cuentaDestino=cuentaDestino, cedula=cedulaUsuario, monto=monto)

    if cuentasOrigen.saldo<valorTransferencia:
        print("No tienes saldo disponible")
    else:

        cuentasOrigen.saldo = cuentasOrigen.saldo-valorTransferencia
        cuentasDestino.saldo = cuentasDestino.saldo+valorTransferencia

    db.session.add(nuevaTransaccion)
    db.session.commit()

    return render_template('dashboard.html', usuario=inicioUsuario)



@app.route('/download')
def descargar():
    # Crear una instancia de FPDF
    pdf = FPDF()
    pdf.add_page()

    # Configurar la fuente
    pdf.set_font("Arial", size=12)

    # Añadir un encabezado
    pdf.cell(0, 10, "Documento PDF con fpdf", ln=True, align='C')

    # Obtener transacciones del usuario (asegúrate que `inicioUsuario` está definido y tiene `cedula`)
    usuario_id = inicioUsuario.cedula
    listaTransacciones = Transaccion.query.filter_by(cedula=usuario_id).all()

    # Cabecera de la tabla
    pdf.cell(40, 10, 'Cédula', 1)
    pdf.cell(50, 10, 'Cuenta Origen', 1)
    pdf.cell(30, 10, 'Monto', 1)
    pdf.cell(60, 10, 'Fecha', 1)
    pdf.ln()

    # Añadir datos de transacciones
    for transaccion in listaTransacciones:
        pdf.cell(40, 10, transaccion.cedula, 1)
        pdf.cell(50, 10, transaccion.cuentaOrigen, 1)
        pdf.cell(30, 10, f"${float(transaccion.monto):,.2f}", 1)
        pdf.cell(60, 10, transaccion.fechaTransaccion.strftime("%Y-%m-%d %H:%M:%S"), 1)
        pdf.ln()

    # Guardar el archivo PDF en la memoria
    pdf_buffer = io.BytesIO()
    pdf.output(dest='S')
    pdf_buffer.write(pdf.output(dest='S').encode('latin1'))
    pdf_buffer.seek(0)

    # Enviar el archivo PDF en respuesta
    return send_file(pdf_buffer, as_attachment=True, download_name='transacciones.pdf', mimetype='application/pdf')

@app.route('/historial')
def transaccion():

    usuario_id=inicioUsuario.cedula
    listaTransacciones = Transaccion.query.filter_by(cedula=usuario_id).all()
    print(listaTransacciones[0].monto)


    return render_template('transacciones.html', usuario=inicioUsuario, historial=listaTransacciones)
@app.route('/salir')

def salir():
    return redirect('/ingresar')
if __name__ == '__main__':
    app.run(debug=True)