from flask import Flask,render_template, request, session,redirect,url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'havit'

def connect_database():
    conn = sqlite3.connect('nombre.db')
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/usuario')
def usuario():
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute('SELECT id,username, email FROM user')
    datos = cursor.fetchall()
    conn.close()
    
    return render_template('usuario.html', datos=datos)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'] 
        password = request.form['password'] 
        conn = connect_database() 
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE username=? AND password=?', (username, password))
        
        user = cursor.fetchone() 
        conn.close() 
        
        if user:
            session['username'] = username 
            return redirect(url_for('index'))
        else: 
            return render_template('auth/login.html')
    return render_template('auth/login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username'] 
        email = request.form['email']
        password = request.form['password']
        
        session['username'] = username 
        
        conn = connect_database() 
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE username=? OR email=?', (username, email))
        user = cursor.fetchone()
        
        if user:
            conn.close() 
            return render_template('auth/registro.html')
        else:
            cursor.execute('INSERT INTO user (username, email, password) VALUES (?, ?, ?)', (username, email, password))
            conn.commit() 
            conn.close() 

            return redirect(url_for('index'))
    
    return render_template('auth/registro.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/usuario_editar/<int:user_id>', methods=['GET', 'POST'])
def editar_usuario(user_id):
    conn = connect_database()
    cursor = conn.cursor()

    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        contrasena = request.form['contrasena']

        cursor.execute('UPDATE user SET username=?, email=?, password=? WHERE id=?', (nombre, correo, contrasena, user_id))
        conn.commit()
        conn.close()

        return redirect(url_for('usuario'))  # Redirigir al usuario a la página de usuarios después de la edición

    # Obtener los datos del usuario a editar
    cursor.execute('SELECT * FROM user WHERE id=?', (user_id,))
    usuario = cursor.fetchone()
    conn.close()

    if usuario:
        return render_template('editar_usuario.html', usuario=usuario)
    else:
        return redirect(url_for('usuario'))  # Redirigir al usuario a la página de usuarios si el usuario no existe

@app.route('/producto')
def producto():
    conn = connect_database()
    cursor = conn.cursor()

    # Seleccionar todos los datos de la tabla producto
    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()

    conn.close()

    # Renderizar la plantilla HTML producto.html y pasar los datos de los productos
    return render_template('producto.html', productos=productos)


@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        conn = connect_database()
        cursor = conn.cursor()
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        precio = request.form.get('precio')

        cursor.execute('INSERT INTO producto (nombre, descripcion, precio) VALUES (?, ?, ?)', (nombre, descripcion, precio))
        conn.commit()

        conn.close()
        
        return redirect(url_for('producto')) 
    
    return render_template('agregar_producto.html')  


@app.route('/editar_producto/<int:producto_id>', methods=['GET', 'POST'])
def editar_producto(producto_id):
    conn = connect_database()
    cursor = conn.cursor()

    if request.method == 'POST':
        # Manejar la lógica para actualizar el producto en la base de datos
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']

        cursor.execute("UPDATE producto SET nombre=?, descripcion=?, precio=? WHERE id=?", (nombre, descripcion, precio, producto_id))
        conn.commit()
        conn.close()

        return redirect('/producto') 
    else:
        # Consultar la base de datos para obtener los detalles del producto con el ID dado
        cursor.execute("SELECT * FROM producto WHERE id = ?", (producto_id,))
        detalles_producto = cursor.fetchone()
        conn.close()

        return render_template('editar_producto.html', producto_id=producto_id, detalles_producto=detalles_producto)

#
if __name__ == '__main__':
    app.run(debug=True)
