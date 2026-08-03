from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import os
from dotenv import load_dotenv
from werkzeug.security import check_password_hash

load_dotenv()

app = Flask(__name__)
CORS(app)

def obtener_conexion():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_disabled=False
    )
    
@app.route("/login", methods=["POST"])
def login():
    datos = request.get_json()
    usuario = datos.get("usuario")
    contraseña = datos.get("contraseña")
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT contraseña_hash FROM usuarios WHERE usuario = %s", (usuario,))
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    
    if resultado and check_password_hash(resultado[0], contraseña):
        return jsonify({"exito": True}), 200
    else:
        return jsonify({"exito": False}), 401    
    
@app.route("/clientes")
def obtener_clientes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, correo FROM clientes")
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    clientes = []
    for fila in resultados:
        clientes.append({"id": fila[0], "nombre": fila[1], "correo": fila[2]})
        
    return jsonify(clientes)

@app.route("/clientes", methods=["POST"])
def crear_cliente():
    datos = request.get_json()
    nombre = datos.get("nombre")
    correo = datos.get("correo")
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT MAX(id) FROM clientes")
    max_id = cursor.fetchone()[0] or 0
    nuevo_id = max_id + 1
    
    cursor.execute(
        "INSERT INTO clientes (id, nombre, correo) VALUES (%s, %s, %s)",
        (nuevo_id, nombre, correo)
    )
    conexion.commit()
    cursor.close()
    conexion.close()

    return jsonify({"id": nuevo_id, "nombre": nombre, "correo": correo}), 201

@app.route("/clientes/<int:id_cliente>", methods=["DELETE"])
def eliminar_cliente(id_cliente):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = %s", (id_cliente,))
    conexion.commit()
    cursor.close()
    conexion.close()
    
    return jsonify({"mensaje": "Cliente eliminado"}), 200

@app.route("/clientes/<int:id_cliente>", methods=["PUT"])
def actualizar_cliente(id_cliente):
    datos = request.get_json()
    nombre = datos.get("nombre")
    correo = datos.get("correo")
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE clientes SET nombre = %s, correo = %s WHERE id = %s",
        (nombre, correo, id_cliente)
    )
    conexion.commit()
    cursor.close()
    conexion.close()
    
    return jsonify({"id": id_cliente, "nombre": nombre, "correo": correo}), 200

@app.route("/productos/<int:id_producto>", methods=["DELETE"])
def eliminar_producto(id_producto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id_producto,))
    conexion.commit()
    cursor.close()
    conexion.close()
    
    return jsonify({"mensaje": "Producto eliminado"}), 200

@app.route("/pedidos/<int:id_pedido>", methods=["DELETE"])
def eliminar_pedido(id_pedido):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM pedidos WHERE id = %s", (id_pedido,))
    conexion.commit()
    cursor.close()
    conexion.close()
    
    return jsonify({"mensaje": "Pedido eliminado"}), 200

@app.route("/productos")
def obtener_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, precio FROM productos")
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    productos = []
    for fila in resultados:
        productos.append({"id": fila[0], "nombre": fila[1], "precio": float(fila[2])})
        
    return jsonify(productos)

@app.route("/productos", methods=["POST"])
def crear_producto():
    datos = request.get_json()
    nombre = datos.get("nombre")
    precio = datos.get("precio")
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT MAX(id) FROM productos")
    max_id = cursor.fetchone()[0] or 0
    nuevo_id = max_id + 1
    
    cursor.execute(
        "INSERT INTO productos (id, nombre, precio) VALUES (%s, %s, %s)",
        (nuevo_id, nombre, precio)
    )
    conexion.commit()
    cursor.close()
    conexion.close()
    
    return jsonify({"id": nuevo_id, "nombre": nombre, "precio": precio}), 201

@app.route("/pedidos")
def obtener_pedidos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT pedidos.id, pedidos.fecha, clientes.nombre
        FROM pedidos
        JOIN clientes ON pedidos.id_cliente = clientes.id
    """)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()
    
    pedidos = []
    for fila in resultados:
        pedidos.append({"id": fila[0], "fecha": str(fila[1]), "cliente": fila[2]})
        
    return jsonify(pedidos)

@app.route("/pedidos", methods=["POST"])
def crear_pedido():
    datos = request.get_json()
    id_cliente = datos.get("id_cliente")
    fecha = datos.get("fecha")
    
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT MAX(id) FROM pedidos")
    max_id = cursor.fetchone()[0] or 0
    nuevo_id = max_id + 1
    
    cursor.execute(
        "INSERT INTO pedidos (id, id_cliente, fecha) VALUES (%s, %s, %s)",
        (nuevo_id, id_cliente, fecha)
    )
    conexion.commit()
    cursor.close()
    conexion.close()
    
    return jsonify({"id": nuevo_id, "fecha": fecha, "id_cliente": id_cliente}), 201

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')
    
    
    
    
            
