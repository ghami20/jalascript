from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    
    load_dotenv()

    app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
    app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
    app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
    app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

    mysql.init_app(app) 

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/agregar', methods=['GET', 'POST'])
    def agregar_usuario():
        if request.method == 'POST':
            nombre = request.form['nombre']
            email = request.form['email']
            edad = int(request.form['edad'])

            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO usuarios (nombre, email, edad) VALUES (%s, %s, %s)", (nombre, email, edad))
            mysql.connection.commit()
            cursor.close()

            return redirect(url_for('ver_usuarios'))

        return render_template('agregar_usuario.html')

    @app.route('/ver')
    def ver_usuarios():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, nombre, email, edad FROM usuarios")
        usuarios = cursor.fetchall()
        cursor.close()
        return render_template('ver_usuarios.html', usuarios=usuarios)

    @app.route('/editar/<int:id>', methods=['GET', 'POST'])
    def editar_usuario(id):
        cursor = mysql.connection.cursor()
        if request.method == 'POST':
            nombre = request.form['nombre']
            email = request.form['email']
            edad = int(request.form['edad'])

            cursor.execute("UPDATE usuarios SET nombre = %s, email = %s, edad = %s WHERE id = %s", (nombre, email, edad, id))
            mysql.connection.commit()
            cursor.close()

            return redirect(url_for('ver_usuarios'))

        cursor.execute("SELECT nombre, email, edad FROM usuarios WHERE id = %s", (id,))
        usuario = cursor.fetchone()
        cursor.close()
        return render_template('editar_usuario.html', usuario=usuario)

    @app.route('/eliminar/<int:id>', methods=['POST'])
    def eliminar_usuario(id):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('ver_usuarios'))

    @app.route('/buscar', methods=['GET', 'POST'])
    def buscar_por_edad():
        usuarios = []
        if request.method == 'POST':
            edad = int(request.form['edad'])
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT id, nombre, email, edad FROM usuarios WHERE edad = %s", (edad,))
            usuarios = cursor.fetchall()
            cursor.close()
        
        return render_template('buscar_usuarios.html', usuarios=usuarios)

    return app

if __name__ == '__main__':
    create_app().run(debug=True)
