from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# 1. Configuración de conexión a MariaDB (HeidiSQL)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456' # Contraseña corregida según tu configuración
app.config['MYSQL_DB'] = 'logicon'

# 2. Inicialización de MySQL (Debe ir antes de las rutas)
mysql = MySQL(app)

# --- RUTAS DE NAVEGACIÓN GENERAL ---

@app.route('/')
def home():
    return render_template('index.html')

# --- RUTAS DE PRODUCTOS ---

@app.route('/productos')
def productos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_prod, nombre, precio, stock FROM PRODUCTO")
    datos = cur.fetchall() 
    cur.close()
    return render_template('productos.html', inventario=datos)

@app.route('/agregar', methods=['POST'])
def agregar_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        stock = request.form['stock']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO PRODUCTO (nombre, precio, stock) VALUES (%s, %s, %s)", 
                    (nombre, precio, stock))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('productos'))

@app.route('/eliminar/<id>')
def eliminar_producto(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM PRODUCTO WHERE id_prod = %s", (id,))
    mysql.connection.commit()
    cur.close()
    # Corregido: redirigir a la función 'productos'
    return redirect(url_for('productos'))

# --- RUTAS DE CLIENTES ---

@app.route('/clientes')
def listar_clientes():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id_cliente, razon_social, telefono, tipo_cliente FROM CLIENTE")
    datos_clientes = cur.fetchall()
    cur.close()
    return render_template('clientes.html', clientes=datos_clientes)

if __name__ == '__main__':
    app.run(debug=True)