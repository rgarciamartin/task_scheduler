import warnings

from backend.tasks.tests.utils import TaskTestUtils
from django.contrib.auth.models import User

warnings.filterwarnings("ignore", category=RuntimeWarning)
print("> Creando super usuario demo:demo")
user = User(username="demo", email="demo@example.com", is_staff=True, is_superuser=True)
user.set_password("demo")
user.save()

print("> Creando tareas de prueba")
# Tarea 1
TaskTestUtils.create_task(
    owner_id=user.id,
    title="Realizar Presentación",
    description="Preparar diapositivas para la reunión.",
    status="to_do",
)

# Tarea 2
TaskTestUtils.create_task(
    owner_id=user.id,
    title="Llamar al Cliente",
    description="Confirmar detalles.",
    status="in_progress",
)

# Tarea 3
TaskTestUtils.create_task(
    owner_id=user.id,
    title="Revisar Documentación",
    description="Evaluación estado de los transportes.",
    status="completed",
)

# Tarea 4
TaskTestUtils.create_task(
    owner_id=user.id,
    title="Enviar Facturas",
    description="Facturación del mes de Noviembre.",
    status="stand_by",
)


print("----------------------------")
print(" - Datos generados correctamente -")
print(" Ya se puede consultar la api generando el token")
print(" Con el usuario: 'demo' y contraseña: 'demo'")
print("----------------------------")
