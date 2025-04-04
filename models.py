from flask_sqlalchemy import SQLAlchemy

# Instancia de SQLAlchemy
db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    # Definición de los campos de la tabla
    cedula = db.Column(db.String(20), primary_key=True)
    nombre = db.Column(db.String(30), nullable=False)
    usuario = db.Column(db.String(50), nullable=False)
    contrasena = db.Column(db.String(100), nullable=False)
    activa = db.Column(db.Boolean, default=True)
    intentos = db.Column(db.Integer, default=0)

    def __init__(self, cedula, nombre, usuario, contrasena, fechaRegistro):
        self.cedula = cedula
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena
        self.fechaRegistro = fechaRegistro

    def __repr__(self):
        return f'<Usuario {self.nombre}>'

class Cuenta(db.Model):
    __tablename__ = 'cuentas'

    numeroCuenta = db.Column(db.String(20), primary_key=True)
    tipoCuenta = db.Column(db.String(50), nullable=False)
    saldo = db.Column(db.Numeric(15, 2), nullable=False, default=0.00)
    cedula = db.Column(db.String(20), db.ForeignKey('usuarios.cedula'), nullable=False)

    def __init__(self, numeroCuenta, tipoCuenta, saldo, cedula, fechaRegistroCuenta):
        self.numeroCuenta = numeroCuenta
        self.tipoCuenta = tipoCuenta
        self.saldo = saldo
        self.cedula = cedula
        self.fechaRegistroCuenta = fechaRegistroCuenta

    def __repr__(self):
        return f'<Cuenta {self.numeroCuenta} - Tipo: {self.tipoCuenta}>'

class Transaccion(db.Model):
    __tablename__ = 'transacciones'

    # Definición de los campos de la tabla
    idTransaccion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cuentaOrigen = db.Column(db.String(20), db.ForeignKey('cuentas.numeroCuenta'), nullable=False)
    cuentaDestino = db.Column(db.String(20), db.ForeignKey('cuentas.numeroCuenta'), nullable=False)
    cedula = db.Column(db.String(20), db.ForeignKey('usuarios.cedula'), nullable=False)
    monto = db.Column(db.Numeric(15, 2), nullable=False)
    fechaTransaccion = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, cuentaOrigen, cuentaDestino, cedula, monto):
        self.cuentaOrigen = cuentaOrigen
        self.cuentaDestino = cuentaDestino
        self.cedula = cedula
        self.monto = monto

    def __repr__(self):
        return f'<Transaccion {self.idTransaccion}: {self.monto} de {self.cuentaOrigen} a {self.cuentaDestino}>'