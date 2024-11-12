from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os

mysql = MySQL()  # Crear instancia de MySQL fuera de create_app

def create_app():
    app = Flask(__name__)

    # Configuración de MySQL usando variables de entorno
    app.config["MYSQL_USER"] = os.getenv("MYSQL_USER", "u634693279_ghami")
    app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD", "Ghami1234")
    app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST", "srv1601.hstgr.io")
    app.config["MYSQL_DB"] = os.getenv("MYSQL_DB", "u634693279_davinciguesser")

    mysql.init_app(app)  # Inicializar MySQL con la aplicación

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/agregar', methods=['GET', 'POST'])
    def agregar_usuario_mysql():
        if request.method == 'POST':
            nombre = request.form['nombre']
            email = request.form['email']
            edad = int(request.form['edad'])

            # Insertar datos en MySQL
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, email, edad) VALUES (%s, %s, %s)", (nombre, email, edad))
            mysql.connection.commit()
            cursor.close()

            return redirect(url_for('ver_usuarios_mysql'))

        return render_template('agregar_usuario.html')

    @app.route('/ver')
    def ver_usuarios_mysql():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT nombre, email, edad FROM usuarios")
        usuarios = cursor.fetchall()
        cursor.close()
        return render_template('ver_usuarios.html', usuarios=usuarios)

    return app

# Solo para desarrollo local
if __name__ == '__main__':
    create_app().run(debug=True)
