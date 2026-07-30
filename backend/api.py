from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from flask import request
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=os.getenv("DB_PASSWORD"),
        database="tienda"
    )
    
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
    app.run(debug=True, port=5000)
    
    
    
            
