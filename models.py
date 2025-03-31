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

    def __init__(self, cedula, nombre, usuario, contrasena, fechaRegistro):
        self.cedula = cedula
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena
        self.fechaRegistro = fechaRegistro

    def obtenerUsuario(usuario, contrasena):

        return Usuario.query.filter_by(usuario=usuario, contrasena=contrasena).first()

        #return self.query.filter_by(usuario=usuario).first()

    def __repr__(self):
        return f'<Usuario {self.nombre}>'