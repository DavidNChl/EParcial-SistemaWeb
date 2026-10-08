const API = '/api/licores';
const ADMIN_KEY = 'licoreria-admin-2026';
const tbody = document.getElementById('liquor-tbody');

const AUTH_HEADERS = {
  'Content-Type': 'application/json',
  'X-API-Key': ADMIN_KEY
};

// Cargar datos desde la API
async function loadLicores() {
  const res = await fetch(API);
  const json = await res.json();
  if (json.success) render(json.data);
}

// Renderizar filas en la tabla
function render(items) {
  tbody.innerHTML = '';
  items.forEach(item => {
    const tr = document.createElement('tr');

    const tdNombre = document.createElement('td');
    tdNombre.textContent = item.nombre;

    const tdCat = document.createElement('td');
    tdCat.innerHTML = `<span class="badge">${item.categoria}</span>`;

    const tdPrecio = document.createElement('td');
    tdPrecio.textContent = `S/ ${parseFloat(item.precio).toFixed(2)}`;

    const tdStock = document.createElement('td');
    tdStock.textContent = `${item.stock} u.`;
    if (item.stock_critico) {
      tdStock.innerHTML += ` <span class="badge alert-stock">¡Bajo!</span>`;
    }

    const tdAcciones = document.createElement('td');

    // Redirección a la vista de edición con el ID en el Query Parameter
    const btnEdit = document.createElement('button');
    btnEdit.textContent = 'Editar';
    btnEdit.className = 'btn-edit';
    btnEdit.onclick = () => {
      window.location.href = `/editar?id=${item.id}`;
    };

    const btnDel = document.createElement('button');
    btnDel.textContent = 'Eliminar';
    btnDel.className = 'btn-danger';
    btnDel.onclick = () => deleteLicor(item.id);

    tdAcciones.appendChild(btnEdit);
    tdAcciones.appendChild(btnDel);

    tr.appendChild(tdNombre);
    tr.appendChild(tdCat);
    tr.appendChild(tdPrecio);
    tr.appendChild(tdStock);
    tr.appendChild(tdAcciones);

    tbody.appendChild(tr);
  });
}

// Crear licor (POST)
document.getElementById('create-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const payload = {
    nombre: document.getElementById('create-nombre').value,
    categoria: document.getElementById('create-categoria').value,
    precio: parseFloat(document.getElementById('create-precio').value),
    stock: parseInt(document.getElementById('create-stock').value),
    grado_alcohol: parseFloat(document.getElementById('create-grado').value || 0)
  };

  const res = await fetch(API, {
    method: 'POST',
    headers: AUTH_HEADERS,
    body: JSON.stringify(payload)
  });

  if (res.ok) {
    document.getElementById('create-form').reset();
    loadLicores();
  } else {
    alert('Error al agregar el producto. Verifica tus permisos.');
  }
});

// Eliminar licor (DELETE)
async function deleteLicor(id) {
  if (!confirm('¿Desea eliminar este producto?')) return;
  const res = await fetch(`${API}/${id}`, {
    method: 'DELETE',
    headers: { 'X-API-Key': ADMIN_KEY }
  });

  if (res.ok) {
    loadLicores();
  } else {
    alert('Error al eliminar el producto.');
  }
}

loadLicores();