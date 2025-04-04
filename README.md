# AppBancaria Sistema de Gestión Bancaria

Este proyecto es una aplicación web que permite la gestión bancaria, incluyendo el registro de usuarios, transacciones y generación de reportes en formato PDF.

## Tabla de Contenidos
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Modelos de Base de Datos](#modelos-de-base-de-datos)
- [Rutas](#rutas)
- [Contribución](#contribución)
- [Licencia](#licencia)
- [Contacto](#contacto)
- [Créditos](#créditos)

## Requisitos

- Python 3.x
- Virtualenv (opcional pero recomendado)

## Instalación

1. Clona el repositorio:
   ```bash
   git clone git@github.com:Aandress712/AppBancaria.git
   cd AppBancaria
 
2. Crea un entorno virtual e instálalo (opcional):

   ``` python
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   .\venv\Scripts\activate   # En Windows

3. Instala las dependencias:

   ``` python
    pip install -r requirements.txt

4. Configura la base de datos y crea las tablas necesarias:

    Asegúrate de configurar tus credenciales en config.py antes de ejecutar:

   ``` psql
    Config.SQLALCHEMY_DATABASE_URI = 'tu_uri_de_base_de_datos'

## Uso

    Abre tu navegador y navega a http://127.0.0.1:5000/.
    Regístrate y crea una cuenta bancaria.
    Realiza transacciones y verifica el historial.
    Descarga reportes en PDF de tus transacciones.

## Modelos de Base de Datos
    # Usuario:

        cedula: String(20), clave primaria.
        nombre: String(30).
        usuario: String(50).
        contrasena: String(100).
        activa: Boolean (predeterminado True).
        intentos: Integer (predeterminado 0).

    # Cuenta:

        numeroCuenta: String(20), clave primaria.
        tipoCuenta: String(50).
        saldo: Numeric (15, 2).
        cedula: String(20), clave foránea de Usuario.

    # Transaccion:

        idTransaccion: Integer, clave primaria.
        cuentaOrigen: String(20), clave foránea de Cuenta.
        cuentaDestino: String(20), clave foránea de Cuenta.
        cedula: String(20), clave foránea de Usuario.
        monto: Numeric (15, 2).
        fechaTransaccion: DateTime (predeterminado current_timestamp).

## Rutas

    /: Página de inicio.
    /registrar_usuario: Ruta para registrar un nuevo usuario.
    /iniciar-sesion: Ruta para iniciar sesión.
    /registrar-cuenta: Ruta para registrar una nueva cuenta bancaria.
    /retiro: Ruta para realizar un retiro.
    /transaccion: Muestra opciones para realizar transferencias.
    /download: Genera y descarga un reporte PDF.
    /historial: Muestra el historial de transacciones.
## Contribución
    
    Haz un fork del proyecto.
    Crea una nueva rama (git checkout -b feature/nueva-feature).
    Realiza tus cambios y haz un commit (git commit -m 'Añadir nueva feature').
    Sube tus cambios (git push origin feature/nueva-feature).
    Abre un Pull Request.
## Licencia

    Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

## Contacto
    Andres Giraldo - 712andres@gmail.com



