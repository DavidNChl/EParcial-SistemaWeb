# Licorería Central - Sistema Web de Gestión de Inventario

## 1. Descripción

**Licorería Central** es una aplicación web para la gestión básica de inventario de productos de una licorería. Permite consultar, registrar, editar y eliminar licores mediante una interfaz web dinámica conectada de forma asíncrona a una API REST.

El proyecto fue desarrollado para evidenciar los conceptos de las primeras semanas del curso de Desarrollo de Aplicaciones Web: HTML5/CSS3, JavaScript Vanilla, Fetch API, JSON, arquitectura modular, Programación Orientada a Objetos, principios SOLID y medidas básicas de seguridad web.

## 2. Tecnologías utilizadas

### Frontend

* HTML5.
* CSS3 con diseño adaptable mediante CSS Grid y `viewport` responsive.
* JavaScript Vanilla.
* Fetch API y `async/await`.
* JSON para el intercambio de información con el backend.
* Manipulación dinámica del DOM.

### Backend

* Python 3.
* FastAPI.
* Pydantic.
* Peewee ORM.
* SQLite.
* Passlib con bcrypt para hashing de contraseñas.

## 3. Estructura del proyecto

```text
EParcial-SistemaWeb-main/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── services.py
├── repository.py
├── requirements.txt
├── licoreria.db
└── static/
    ├── index.html
    └── editar.html
```

### Responsabilidad de cada módulo

| Archivo              | Responsabilidad                                                     |
| -------------------- | ------------------------------------------------------------------- |
| `main.py`            | Configuración de FastAPI, rutas REST y publicación del frontend.    |
| `database.py`        | Configuración de la conexión SQLite mediante Peewee.                |
| `models.py`          | Entidades `LiquorModel`, `UserModel` y clase base ORM.              |
| `schemas.py`         | Validación de datos de entrada con Pydantic.                        |
| `services.py`        | Reglas de negocio y sanitización de texto.                          |
| `repository.py`      | Acceso a datos y operaciones CRUD mediante Peewee.                  |
| `static/index.html`  | Interfaz principal, estilos, formularios y JavaScript del frontend. |
| `static/editar.html` | Interfaz auxiliar para consultar y editar un producto por ID.       |

## 4. Requisitos

* Python 3.10 o superior.
* `pip`.
* Navegador web moderno.

## 5. Instalación

### 5.1 Clonar o descargar el repositorio

Colocar el proyecto en una carpeta local y abrir una terminal en la raíz del proyecto.

### 5.2 Crear y activar un entorno virtual (recomendado)

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 5.3 Instalar dependencias

```bash
pip install -r requirements.txt
```

## 6. Ejecución

Desde la raíz del proyecto:

```bash
uvicorn main:app --reload
```

Luego abrir en el navegador:

```text
http://127.0.0.1:8000/
```

La documentación automática de FastAPI queda disponible en:

```text
http://127.0.0.1:8000/docs
```

## 7. Funcionalidades

### Consulta

* Listado de todos los licores.
* Consulta de un licor por ID.
* Indicador visual de `stock_critico` cuando el stock es menor a 5 unidades.

### Registro

* Alta de nuevos productos mediante formulario.
* Envío de los datos mediante `POST` y JSON.

### Edición

* Edición desde el modal de la página principal.
* Actualización mediante `PUT`.

### Eliminación

* Confirmación del usuario antes de eliminar.
* Eliminación mediante `DELETE`.

## 8. Endpoints REST

| Método   | Ruta                      | Descripción                      |
| -------- | ------------------------- | -------------------------------- |
| `GET`    | `/api/licores`            | Lista todos los productos.       |
| `GET`    | `/api/licores/{licor_id}` | Consulta un producto específico. |
| `POST`   | `/api/licores`            | Registra un nuevo producto.      |
| `PUT`    | `/api/licores/{licor_id}` | Actualiza un producto.           |
| `DELETE` | `/api/licores/{licor_id}` | Elimina un producto.             |

Ejemplo de JSON para crear un licor:

```json
{
  "nombre": "Pisco Quebranta 750ml",
  "categoria": "Pisco",
  "precio": 48.0,
  "stock": 12,
  "grado_alcohol": 42.0
}
```

## 9. Validación y seguridad

El backend valida las entradas con Pydantic antes de ejecutar la lógica de negocio. Por ejemplo:

* `nombre`: entre 2 y 100 caracteres.
* `precio`: mayor que 0.
* `stock`: mayor o igual a 0.
* `grado_alcohol`: mayor o igual a 0.

Los campos de texto `nombre` y `categoria` se limpian y escapan mediante `html.escape()` en la capa de servicios para reducir el riesgo de XSS.

El frontend utiliza `textContent` para renderizar el nombre del producto y construye los botones dinámicamente. El acceso a datos utiliza Peewee ORM.

El modelo `UserModel` incorpora `passlib` con esquema bcrypt y almacena la contraseña en `password_hash` en lugar de guardar la contraseña directamente en texto plano.

> Nota de alcance: el proyecto actual implementa el modelo y las funciones de hashing para usuarios, pero no expone un flujo completo de registro/login en la interfaz de la aplicación.

## 10. Arquitectura y SOLID

El backend separa responsabilidades en capas:

```text
Cliente / Navegador
        |
        v
     FastAPI
    (main.py)
        |
        v
  Capa de servicios
   (services.py)
        |
        v
    Repository
  (repository.py)
        |
        v
      Peewee
        |
        v
     SQLite
```

Esta separación facilita mantenimiento, pruebas y evolución del proyecto. El principio más evidente es **Responsabilidad Única (SRP)**: las rutas, validación, lógica de negocio, acceso a datos y modelos se mantienen en módulos distintos.

## 11. Datos iniciales

Al iniciar la aplicación, `main.py` crea las tablas `licores` y `usuarios` si no existen. Si la tabla `licores` está vacía, se insertan dos productos iniciales de demostración.

## 12. Comprobación rápida

1. Ejecutar el servidor.
2. Abrir `/`.
3. Verificar los productos iniciales.
4. Registrar un producto.
5. Editarlo.
6. Eliminarlo.
7. Abrir `/docs` y comprobar los endpoints REST.
8. Revisar la pestaña **Network** del navegador para observar `GET`, `POST`, `PUT` y `DELETE`.

## 13. Archivos recomendados para el repositorio

Para la entrega académica se recomienda conservar:

* Código fuente.
* `README.md`.
* `requirements.txt`.
* Manual técnico en PDF.
* Base de datos de demostración, si el docente solicita entregarla.

No se deben subir contraseñas reales, claves secretas ni información sensible.
