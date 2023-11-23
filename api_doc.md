# Documentación de la API

## Autenticación

Para poder acceder a la API, es necesario autenticarse:

**Endpoint:** `/api/v1/auth/token/`

**Method:** `POST`

**Body:**

- `username` (str): Nombre de usuario.
- `password` (str): Contraseña.

**Response:**

- Status code: 200 - OK
- Body: JSON con el token del usuario.

---

## Tareas

### Listar Tareas

Lista paginada con el listao de tareas para el usuario.

**Endpoint:** `/api/v1/tasks/list/`

**Method:** `GET`

**Headers:**

- `Authorization`: Token de autenticación de la API.

**Response:**

- Status code: 200 - OK
- Body: Lista paginada que contiene diccionarios con las siguientes claves:
  - `uuid` (str): UUID.
  - `title` (str): Título.
  - `created` (str): Marca de tiempo que indica el momento de creación.
  - `last_updated` (str): Marca de tiempo que indica el momento de última actualización.
  - `status` (str): Estado.

---

### Crear Tarea

Crea una nueva tarea.

**Endpoint:** `/api/v1/tasks/create/`

**Method:** `POST`

**Headers:**

- `Authorization`: Token de autenticación de la API.

**Body:**

- `title` (str): Título
- `description` (str): Descripción (no requerido)
- `status` (str): Estado

**Response:**

- Status code: 201 - Created
- Body: Un objeto JSON con el UUID de la tarea.

---

### Actualizar Tarea

Actualiza una tarea ya existente.

**Endpoint:** `/api/v1/tasks/update/{task_uuid}/`

**Method:** `POST`

**Headers:**

- `Authorization`: Token de autenticación de la API.

**Body:**

- `title` (cadena): Título actualizado.
- `description` (cadena): Descripción actualizada.
- `status` (cadena): Estado actualizado.

**Response:**

- Status code: 204 - No Content

---

### Eliminar Tarea

Elimina una tarea.

**Endpoint:** `/api/v1/tasks/delete/{task_uuid}/`

**Method:** `DELETE`

**Headers:**

- `Authorization`: Token de autenticación de la API.

**Response:**

- Status code: 204 - No Content

---
