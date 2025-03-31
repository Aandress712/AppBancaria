import os

class Config:
    # Configuración para la conexión a la base de datos
    SQLALCHEMY_DATABASE_URI = 'postgresql://root:1234@172.17.0.2:5432/bd_appbancaria'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desactivar el seguimiento de modificaciones para optimizar rendimiento