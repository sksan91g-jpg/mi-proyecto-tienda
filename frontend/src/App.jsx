import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [clientes, setClientes] = useState([])
  const [productos, setProductos] = useState([])
  const [pedidos, setPedidos] = useState([])

  const [nombre, setNombre] = useState('')
  const [correo, setCorreo] = useState('')

  const [nombreProducto, setNombreProducto] = useState('')
  const [precioProducto, setPrecioProducto] = useState('')

  const [idClientePedido, setIdClientePedido] = useState('')
  const [fechaPedido, setFechaPedido] = useState('')

  function cargarClientes() {
    fetch('http://127.0.0.1:5000/clientes')
      .then(response => response.json())
      .then(data => setClientes(data))
  }

  function cargarProductos() {
    fetch('http://127.0.0.1:5000/productos')
      .then(response => response.json())
      .then(data => setProductos(data))
  }

  function cargarPedidos() {
    fetch('http://127.0.0.1:5000/pedidos')
      .then(response => response.json())
      .then(data => setPedidos(data))
  }

  useEffect(() => {
    cargarClientes()
    cargarProductos()
    cargarPedidos()
  }, [])

  function agregarCliente() {
    fetch('http://127.0.0.1:5000/clientes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombre, correo })
    })
      .then(response => response.json())
      .then(() => {
        setNombre('')
        setCorreo('')
        cargarClientes()
      })
  }

  function agregarProducto() {
    fetch('http://127.0.0.1:5000/productos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombre: nombreProducto, precio: precioProducto })
    })
      .then(response => response.json())
      .then(() => {
        setNombreProducto('')
        setPrecioProducto('')
        cargarProductos()
      })
  }

  function agregarPedido() {
    fetch('http://127.0.0.1:5000/pedidos', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id_cliente: idClientePedido, fecha: fechaPedido })
    })
      .then(response => response.json())
      .then(() => {
        setIdClientePedido('')
        setFechaPedido('')
        cargarPedidos()
      })
  }

  function enviarPorWhatsapp(pedido) {
    const mensaje = `Pedido #${pedido.id}\nCliente: ${pedido.cliente}\nFecha: ${pedido.fecha}`
    const url = `https://wa.me/?text=${encodeURIComponent(mensaje)}`
    window.open(url, '_blank')
}

  return (
    <div>
      <h1>Lista de clientes</h1>

      <input
        type="text"
        placeholder="Nombre"
        value={nombre}
        onChange={(e) => setNombre(e.target.value)}
      />
      <input
        type="text"
        placeholder="Correo"
        value={correo}
        onChange={(e) => setCorreo(e.target.value)}
      />
      <button onClick={agregarCliente}>Agregar cliente</button>

      <ul>
        {clientes.map((cliente) => (
          <li key={cliente.id}>
            {cliente.nombre} - {cliente.correo}
          </li>
        ))}
      </ul>

      <h1>Lista de productos</h1>

      <input
        type="text"
        placeholder="Nombre del producto"
        value={nombreProducto}
        onChange={(e) => setNombreProducto(e.target.value)}
      />
      <input
        type="number"
        placeholder="Precio"
        value={precioProducto}
        onChange={(e) => setPrecioProducto(e.target.value)}
      />
      <button onClick={agregarProducto}>Agregar producto</button>

      <ul>
        {productos.map((producto) => (
          <li key={producto.id}>
            {producto.nombre} - ${producto.precio}
          </li>
        ))}
      </ul>

      <h1>Lista de pedidos</h1>

      <select
        value={idClientePedido}
        onChange={(e) => setIdClientePedido(e.target.value)}
      >
        <option value="">Selecciona un cliente</option>
        {clientes.map((cliente) => (
          <option key={cliente.id} value={cliente.id}>
            {cliente.nombre}
          </option>
        ))}
      </select>
      <input
        type="date"
        value={fechaPedido}
        onChange={(e) => setFechaPedido(e.target.value)}
      />
      <button onClick={agregarPedido}>Agregar pedido</button>

      <ul>
    {pedidos.map((pedido) => (
      <li key={pedido.id}>
        Pedido #{pedido.id} - {pedido.cliente} - {pedido.fecha}
        <button onClick={() => enviarPorWhatsapp(pedido)}>
          Enviar por WhatsApp
        </button>
      </li>
    ))}
</ul>
    </div>
  )
}

export default App
