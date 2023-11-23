# Tasks Scheduler

### Descripción del proyecto

El proyecto consta en un gestor de tareas, el cual permite:

- Crear, actualizar y eliminar tareas.

- Listado de las tareas asignadas

  - Permite búsqueda por título, estado y fecha de creación

- Acceso restringido

  - Los usuarios solo pueden acceder a sus tareas

### Estructura

La estructura utilizada está basada en el proyecto que estoy trabajando a día de hoy, la cuál, está dando muy buenos resultados y feedback del equipo.
El objetivo principial de esta estructura es reducir el acomplamiento y dependencia, además de mejorar la mantenibilidad.
Cabe destacar que la arquitectura no ha sido desarrollada por mí, si no que a la hora de comenzar el proyecto y valorando diferentes opciones, el equipo de trabajo valoramos diferentes opciones y optamos por utilizar esta estructura.

### Configurar el proyecto

##### Variables de entorno

Para configurar las variables hay que copiar el contenido del archivo _/app/.env.orig_ en un archivo .env y sustituir los valores de las variables por valores reales.

```bash
SECRET_KEY=""
ALLOWED_HOSTS="*"
DEBUG=True
DATABASE_HOST=db
DATABASE_NAME=tasks_scheduler_db
DATABASE_USER=tasks_scheduler_user
DATABASE_PASSWORD=tasks_scheduler_pass
DATABASE_PORT=5432
```

##### Arrancar la imagen de docker

```bash
docker compose up --build
```

##### Datos iniciales

Una vez arrancado el contenedor, hay que ejecutar el siguiente comando para generar un usuario demo con datos de prueba.

```bash
docker exec -i tasks_scheduler-web-1 python manage.py shell < scripts/generate_data.py
```

##### Ejecutar tests

```bash
docker exec -it tasks_scheduler-web-1 python manage.py test
```
