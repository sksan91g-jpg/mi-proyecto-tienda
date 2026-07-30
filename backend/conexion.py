import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sereunhackerenelfuturo",
    database="tienda"
)

def ver_clientes():
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, correo FROM clientes")
    for fila in cursor.fetchall():
        print(fila)
    cursor.close()

def agregar_cliente():
    nombre = input("Nombre del cliente: ")
    correo = input("Correo del cliente: ")
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
    print(f"Cliente agregado con id {nuevo_id}")

def ver_pedidos():
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT pedidos.id, pedidos.fecha, clientes.nombre
        FROM pedidos
        JOIN clientes ON pedidos.id_cliente = clientes.id
    """)
    for fila in cursor.fetchall():
        print(fila)
    cursor.close()

def agregar_pedido():
    ver_clientes()
    id_cliente = input("ID del cliente para este pedido: ")
    fecha = input("Fecha del pedido (YYYY-MM-DD): ")
    cursor = conexion.cursor()
    cursor.execute("SELECT MAX(id) FROM pedidos")
    max_id = cursor.fetchone()[0] or 0
    nuevo_id = max_id + 1
    cursor.execute(
        "INSERT INTO pedidos (id, fecha, id_cliente) VALUES (%s, %s, %s)",
        (nuevo_id, fecha, id_cliente)
    )
    conexion.commit()
    cursor.close()
    print(f"Pedido agregado con id {nuevo_id}")

def ver_productos():
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, precio FROM productos")
    for fila in cursor.fetchall():
        print(fila)
    cursor.close()

def agregar_producto():
    nombre = input("Nombre del producto: ")
    precio = input("Precio del producto: ")
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
    print(f"Producto agregado con id {nuevo_id}")

def ver_detalle_pedido():
    ver_pedidos()
    id_pedido = input("¿De qué pedido quieres ver el detalle? (ID): ")
    cursor = conexion.cursor()
    cursor.execute("""
        SELECT productos.nombre, detalle_pedido.cantidad, productos.precio
        FROM detalle_pedido
        JOIN productos ON detalle_pedido.id_producto = productos.id
        WHERE detalle_pedido.id_pedido = %s
    """, (id_pedido,))
    filas = cursor.fetchall()
    if not filas:
        print("Este pedido no tiene productos registrados.")
    for fila in filas:
        print(fila)
    cursor.close()

# Menú principal
while True:
    print("\n1. Ver clientes")
    print("2. Agregar cliente")
    print("3. Ver pedidos")
    print("4. Agregar pedido")
    print("5. Ver productos")
    print("6. Agregar producto")
    print("7. Ver detalle de un pedido")
    print("8. Salir")
    opcion = input("Elige una opción: ")

    if opcion == "1":
        ver_clientes()
    elif opcion == "2":
        agregar_cliente()
    elif opcion == "3":
        ver_pedidos()
    elif opcion == "4":
        agregar_pedido()
    elif opcion == "5":
        ver_productos()
    elif opcion == "6":
        agregar_producto()
    elif opcion == "7":
        ver_detalle_pedido()
    elif opcion == "8":
        break
    else:
        print("Opción inválida")

conexion.close()
