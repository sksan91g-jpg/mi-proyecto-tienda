import { useState, useEffect } from 'react'
import './App.css'

const API_URL = 'http://10.130.106.27:5000'

function App() {
  const [clientes, setClientes] = useState([])
  const [productos, setProductos] = useState([])
  const [pedidos, setPedidos] = useState([])

  const [nombre, setNombre] = useState('')
  const [correo, setCorreo] = useState('')
  const [idClienteEditando, setIdClienteEditando] = useState(null)

  const [nombreProducto, setNombreProducto] = useState('')
  const [precioProducto, setPrecioProducto] = useState('')

  const [idClientePedido, setIdClientePedido] = useState('')
  const [fechaPedido, setFechaPedido] = useState('')

  const [autenticado, setAutenticado] = useState(false)
  const [usuario, setUsuario] = useState('')
  const [contraseña, setContraseña] = useState('')
  const [mostrarContraseña, setMostrarContraseña] = useState(false)

  function iniciarSesion() {
    fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ usuario, contraseña })
    })
      .then(response => response.json())
      .then(data => {
        if (data.exito) {
          setAutenticado(true)
        } else {
          alert('Usuario o contraseña incorrectos')
        }
      })
  }

  function cargarClientes() {
    fetch(`${API_URL}/clientes`)
      .then(response => response.json())
      .then(data => setClientes(data))
  }

  function cargarProductos() {
    fetch(`${API_URL}/productos`)
      .then(response => response.json())
      .then(data => setProductos(data))
  }

  function cargarPedidos() {
    fetch(`${API_URL}/pedidos`)
      .then(response => response.json())
      .then(data => setPedidos(data))
  }

  useEffect(() => {
    if (autenticado) {
      cargarClientes()
      cargarProductos()
      cargarPedidos()
    }
  }, [autenticado])

  function agregarCliente() {
    if (nombre.trim() === '' || correo.trim() === '') {
      alert('Por favor completa nombre y correo')
      return
    }
    fetch(`${API_URL}/clientes`, {
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

  function eliminarCliente(id) {
    if (!confirm('¿Seguro que quieres eliminar este cliente?')) {
      return
    }
    fetch(`${API_URL}/clientes/${id}`, {
      method: 'DELETE'
    })
      .then(() => {
        cargarClientes()
      })
  }

  function comenzarEdicionCliente(cliente) {
    setIdClienteEditando(cliente.id)
    setNombre(cliente.nombre)
    setCorreo(cliente.correo)
  }

  function guardarEdicionCliente() {
    if (nombre.trim() === '' || correo.trim() === '') {
      alert('Por favor completa nombre y correo')
      return
    }
    fetch(`${API_URL}/clientes/${idClienteEditando}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nombre, correo })
    })
      .then(response => response.json())
      .then(() => {
        setNombre('')
        setCorreo('')
        setIdClienteEditando(null)
        cargarClientes()
      })
  }

  function agregarProducto() {
    if (nombreProducto.trim() === '' || precioProducto === '') {
      alert('Por favor completa nombre y precio')
      return
    }
    fetch(`${API_URL}/productos`, {
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

  function eliminarProducto(id) {
    if (!confirm('¿Seguro que quieres eliminar este producto?')) {
      return
    }
    fetch(`${API_URL}/productos/${id}`, {
      method: 'DELETE'
    })
      .then(() => {
        cargarProductos()
      })
  }

  function agregarPedido() {
    if (idClientePedido === '' || fechaPedido === '') {
      alert('Por favor selecciona un cliente y una fecha')
      return
    }
    fetch(`${API_URL}/pedidos`, {
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

  function eliminarPedido(id) {
    if (!confirm('¿Seguro que quieres eliminar este pedido?')) {
      return
    }
    fetch(`${API_URL}/pedidos/${id}`, {
      method: 'DELETE'
    })
      .then(() => {
        cargarPedidos()
      })
  }

  function enviarPorWhatsapp(pedido) {
    const mensaje = `Pedido #${pedido.id}\nCliente: ${pedido.cliente}\nFecha: ${pedido.fecha}`
    const url = `https://wa.me/?text=${encodeURIComponent(mensaje)}`
    window.open(url, '_blank')
  }

  if (!autenticado) {
    return (
      <div>
        <h1>Iniciar sesión</h1>
        <input
          type="text"
          placeholder="Usuario"
          value={usuario}
          onChange={(e) => setUsuario(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter') iniciarSesion() }}
        />
        <input
          type={mostrarContraseña ? "text" : "password"}
          placeholder="Contraseña"
          value={contraseña}
          onChange={(e) => setContraseña(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter') iniciarSesion() }}
        />
        <button type="button" onClick={() => setMostrarContraseña(!mostrarContraseña)}>
          {mostrarContraseña ? "Ocultar" : "Mostrar"}
        </button>
        <button onClick={iniciarSesion}>Ingresar</button>
      </div>
    )
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
      {idClienteEditando ? (
        <button onClick={guardarEdicionCliente}>Guardar cambios</button>
      ) : (
        <button onClick={agregarCliente}>Agregar cliente</button>
      )}

      <ul>
        {clientes.map((cliente) => (
          <li key={cliente.id}>
            {cliente.nombre} - {cliente.correo}
            <button onClick={() => comenzarEdicionCliente(cliente)}>Editar</button>
            <button onClick={() => eliminarCliente(cliente.id)}>Eliminar</button>
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
            <button onClick={() => eliminarProducto(producto.id)}>Eliminar</button>
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
            <button onClick={() => eliminarPedido(pedido.id)}>Eliminar</button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default App
