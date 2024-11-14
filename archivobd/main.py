from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId  
import os
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config["MONGO_URI"] = "mongodb://localhost:27017/ghami"
mongo = PyMongo(app)

from bson.objectid import ObjectId

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ruta para insertar un producto con imagen
@app.route('/insert_product', methods=['GET', 'POST'])
def insert_product():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = float(request.form['precio'])
        categoria = request.form['categoria']
        
        # Obtener la imagen subida
        imagen = request.files.get('imagen')
        
        if imagen and allowed_file(imagen.filename):
            # Guardar la imagen en la carpeta estática
            filename = secure_filename(imagen.filename)
            imagen_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagen.save(imagen_path)

            # Insertar los datos del producto junto con la URL de la imagen
            mongo.db.productos.insert_one({
                "nombre": nombre,
                "precio": precio,
                "categoria": categoria,
                "imagen": f"/static/images/{filename}"  # Guardar la URL de la imagen
            })
            return redirect(url_for('view_products'))
    return render_template('insert_product.html')
# Ruta para ver productos
@app.route('/view_products')
def view_products():
    productos = list(mongo.db.productos.find())
    return render_template('view_products.html', productos=productos)

# Ruta para buscar productos por categoría o rango de precio
@app.route('/search_products', methods=['GET', 'POST'])
def search_products():
    productos = []
    if request.method == 'POST':
        categoria = request.form['categoria']
        precio_min = request.form['precio_min']
        precio_max = request.form['precio_max']
        
        query = {}
        if categoria:
            query['categoria'] = categoria
        if precio_min or precio_max:
            query['precio'] = {}
            if precio_min:
                query['precio']['$gte'] = float(precio_min)
            if precio_max:
                query['precio']['$lte'] = float(precio_max)
        
        productos = list(mongo.db.productos.find(query))
    
    return render_template('search_products.html', productos=productos)

# Ruta principal
@app.route('/')
def home():
    return render_template('home.html')

# Ruta para insertar datos
@app.route('/insert', methods=['GET', 'POST'])
def insert_data():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        if name and age:
            mongo.db.mi_coleccion.insert_one({"name": name, "age": int(age)})
            print("Documento insertado exitosamente")  
            return redirect(url_for('view_data'))
    return render_template('insert.html')

# Ruta para ver datos
@app.route('/view')
def view_data():
    documents = list(mongo.db.mi_coleccion.find())
    return render_template('view.html', documents=documents)

# Ruta para eliminar un dato
@app.route('/delete/<id>', methods=['POST'])
def delete_data(id):
    mongo.db.mi_coleccion.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('view_data'))

if __name__ == '__main__':
    app.run(debug=True)
