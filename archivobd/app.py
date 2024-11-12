from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os

app = Flask(__name__)

# Configuración directa de MySQL usando variables de entorno
app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

mysql = MySQL(app)

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

if __name__ == '__main__':
    app.run(debug=True)
