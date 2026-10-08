const ADMIN_KEY = 'licoreria-admin-2026';
const urlParams = new URLSearchParams(window.location.search);
const licorId = urlParams.get('id');

if (!licorId) {
  alert('ID no especificado.');
  window.location.href = '/';
}

// Cargar datos actuales del producto
async function loadData() {
  const res = await fetch(`/api/licores/${licorId}`);
  if (!res.ok) {
    alert('Producto no encontrado');
    window.location.href = '/';
    return;
  }
  const json = await res.json();
  const item = json.data;

  document.getElementById('nombre').value = item.nombre;
  document.getElementById('categoria').value = item.categoria;
  document.getElementById('precio').value = item.precio;
  document.getElementById('stock').value = item.stock;
  document.getElementById('grado_alcohol').value = item.grado_alcohol;
}

// Enviar actualización con la clave de administración en la cabecera
document.getElementById('edit-form').addEventListener('submit', async (e) => {
  e.preventDefault();

  const payload = {
    nombre: document.getElementById('nombre').value,
    categoria: document.getElementById('categoria').value,
    precio: parseFloat(document.getElementById('precio').value),
    stock: parseInt(document.getElementById('stock').value),
    grado_alcohol: parseFloat(document.getElementById('grado_alcohol').value || 0)
  };

  const res = await fetch(`/api/licores/${licorId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'X-API-Key': ADMIN_KEY
    },
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    alert('Licor actualizado exitosamente');
    window.location.href = '/';
  } else {
    alert('Error al actualizar el producto');
  }
});

loadData();