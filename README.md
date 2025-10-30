# Sistema de Tickets y usuarios

## Descripción General
Sistema de gestión de tickets de soporte técnico que permite a los usuarios crear, gestionar y dar seguimiento a incidencias técnicas. La aplicación está desarrollada con Flask y utiliza MySQL como base de datos, ademas de rutas con API Rest protegidas con un Jason Web Token (JWT).

## Estructura del Proyecto

```
Tickets System/
├── Config/               # Configuración de la base de datos
├── Controllers/          # Controladores de la aplicación
├── Models/               # Modelos de datos
├── Routes/               # Rutas de las APIs
├── Middleware/           # Decorador del token JWT
├── app.py                # Punto de entrada de la aplicación
└── requirements.txt      # Dependencias del proyecto
```

## Roles de Usuario
El sistema maneja tres roles de usuario:
- **Admin**: Acceso completo al sistema, puede gestionar usuarios y todos los tickets.
- **Tecnico** (Técnico): Puede ver y gestionar tickets asignados a él.
- **Usuario**: Puede crear tickets y ver el estado de sus propios tickets.

## Modelos de Datos

### Usuario (User)
Gestiona la información de los usuarios del sistema.
- **Atributos**: id, nombre, apellidos, cedula, contraseña (cifrada)
- **Métodos principales**:
  - Registra un nuevo usuario
  - Inicia sesion para el sistema
  - Crea Tickets
  - Edita Tickets
  - Elimina Tickets

### Ticket
Gestiona la información de los tickets de soporte.
- **Atributos**: id, titulo, descripcion, estado, fecha_creacion, fecha_modificacion, fecha_completado, usuario, tecnico, admin_asignador
- **Métodos principales**:
  - Visualizacion de ticket
  - Asignacion de ticket a un tecnico
  - Editar estado de un ticket
  - Editar prioridad de un ticket

## Rutas Principales

### Autenticación
- `auth/login`: Inicio de sesion
- `auth/register`: Registro de nuevos usuarios

### Tickets
- `/tickets`: Visualización de tickets según el rol
- `/tickets/user`: Tickets por usuarios
- `/tickets/technician`: Tickets asignados a un tecnico
- `/tickets/create`: Creación de tickets
- `/tickets/update/<id>`: Actualización de tickets
- `/tickets/delete/<id>`: Eliminación de tickets

### Usuarios (solo ADMIN)
- `/users`: Gestión de usuarios
- `/users/create`: Creación de usuarios
- `/users/update/<id>`: Actualización de usuarios
- `/users/delete/<id>`: Eliminación de usuarios

## Tecnologías Utilizadas
- **Backend**: Python, Flask
- **Base de Datos**: MySQL
- **Seguridad**: bcrypt para encriptación de contraseñas
- **Autenticación**: JWT token para proteger las rutas API Rest

## Instalación y Configuración

1. Clonar el repositorio
2. Instalar dependencias:
   ```
   pip install -r requirements.txt
   ```
3. Configurar la base de datos en `Config/conection.py`
4. Ejecutar la aplicación, se crearan las tablas de la BD de manera automatica:
   ```
   python app.py
   ```
5. Acceder a la aplicación en `http://localhost:8000` o el host al que se suba o con contenedores en docker

## Flujo de Trabajo

1. Los usuarios se registran en el sistema
2. Los usuarios pueden crear tickets especificando título, descripción y departamento
3. Los administradores pueden asignar tickets a técnicos
4. Los técnicos pueden actualizar el estado de los tickets
5. Los usuarios pueden ver el estado de sus tickets en todo momento

## Seguridad
- Contraseñas encriptadas con bcrypt
- Token JWT unico y reusable para rutas
- Sesiones seguras con Flask
- Validación de permisos según rol de usuario