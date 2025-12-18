# API_EVAL3: Programación Orientada a Objetos

## Evaluación Unidad 3 - Integración API REST con Persistencia en MySQL usando Python

---

## 1. Descripción General

**API_EVAL3** es un proyecto de evaluación académica que demuestra la integración completa de una arquitectura de software moderna basada en **Programación Orientada a Objetos (POO)**.

El proyecto consume la API pública **JSONPlaceholder** para obtener datos de usuarios y publicaciones (posts), los procesa mediante clases y servicios especializados, y finalmente los persiste en una base de datos **MySQL**.

### Objetivos educativos:

- Aplicar conceptos fundamentales de Programación Orientada a Objetos
- Consumir y procesar datos desde una API REST externa
- Implementar persistencia de datos en MySQL
- Demostrar separación de responsabilidades mediante arquitectura en capas
- Practicar buenas prácticas de desarrollo de software

---

## 2. Arquitectura del Proyecto

El proyecto está organizado en **capas**, cada una con responsabilidades específicas:

```
API_EVAL3
├── app/
│   ├── api/                  # Capa de integración con API externa
│   │   └── jsonplaceholder_client.py
│   │
│   ├── modelos/              # Capa de modelos de dominio
│   │   ├── usuario.py
│   │   └── post.py
│   │
│   ├── services/             # Capa de lógica de negocio
│   │   ├── usuario_service.py
│   │   └── post_service.py
│   │
│   ├── config/               # Capa de configuración
│   │   ├── conexion.py       # Gestión de conexión a BD
│   │   └── settings.py       # Variables de configuración
│   │
│   └── main.py               # Punto de entrada (orquestación)
│
├── datos/
│   └── ddl.sql               # Definición de estructura de BD
│
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Este archivo
```

### Relación con Programación Orientada a Objetos:

| Componente | Concepto POO | Descripción |
|-----------|-------------|-------------|
| **Modelos** (usuario.py, post.py) | Clases | Representan entidades del dominio |
| **Servicios** (usuario_service.py, post_service.py) | Métodos de clase, Inyección de dependencias | Coordinan la lógica de negocio |
| **Cliente API** (jsonplaceholder_client.py) | Encapsulación | Abstrae la comunicación HTTP |
| **Conexión** (conexion.py) | Manejo de recursos | Gestiona el ciclo de vida de la conexión |

---

## 3. Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|-----------|---------|----------|
| **Python** | 3.8+ | Lenguaje principal |
| **MySQL** | 5.7+ | Base de datos relacional |
| **WampServer** | 3.2.x | Servidor local con MySQL integrado |
| **requests** | 2.28+ | Cliente HTTP para consumir API |
| **mysql-connector-python** | 8.0+ | Conector MySQL para Python |
| **JSONPlaceholder** | - | API REST pública de pruebas |
| **GitHub Copilot** | - | Asistencia en desarrollo |
| **Visual Studio Code** | - | Editor de código |

---

## 4. Conceptos de POO Aplicados

### 4.1 Clases y Objetos

```python
class Usuario:
    def __init__(self, id: int, nombre: str, correo: str):
        self.id = id
        self.nombre = nombre
        self.correo = correo
```

Las clases `Usuario` y `Post` representan entidades del dominio. Cada instancia es un objeto independiente.

### 4.2 Constructores

```python
def __init__(self, cliente: JsonPlaceholderClient, conexion: Conexion):
    self.cliente = cliente
    self.conexion = conexion
```

Los constructores inicializan el estado del objeto mediante **inyección de dependencias**.

### 4.3 Métodos de Clase (@classmethod)

```python
@classmethod
def from_dict(cls, data: dict) -> 'Usuario':
    return cls(
        id=data['id'],
        nombre=data['name'],
        correo=data['email']
    )
```

Los métodos de clase permiten crear instancias a partir de diccionarios (JSON).

### 4.4 Encapsulación

```python
def _obtener_usuarios_api(self) -> List[Usuario]:
    # Método privado (convención: prefijo _)
```

Los métodos privados (con prefijo `_`) encapsulan detalles internos no expuestos públicamente.

### 4.5 Separación de Responsabilidades

Cada clase tiene un propósito específico:

- **JsonPlaceholderClient**: Comunicación con API
- **Usuario / Post**: Representación de datos
- **UsuarioService / PostService**: Lógica de negocio
- **Conexion**: Gestión de conexiones
- **main.py**: Orquestación del flujo

---

## 5. Flujo de Funcionamiento

### Fase 1: Obtención de datos desde API

```
JSONPlaceholder API
        ↓
JsonPlaceholderClient.get_usuarios()
        ↓
Lista de diccionarios JSON
```

### Fase 2: Conversión a objetos

```
Diccionarios JSON
        ↓
Usuario.from_dict() / Post.from_dict()
        ↓
Objetos Usuario y Post
```

### Fase 3: Persistencia en BD

```
Objetos
        ↓
UsuarioService.importar_desde_api()
        ↓
Conexion.obtener_conexion()
        ↓
INSERT INTO usuario ...
        ↓
MySQL (api_eval3)
```

### Fase 4: Consulta y recuperación

```
SELECT * FROM usuario
        ↓
Filas de BD
        ↓
Usuario.from_dict() para cada fila
        ↓
Lista de objetos Usuario
```

---

## 6. Instrucciones de Ejecución

### 6.1 Requisitos previos

- Python 3.8 o superior instalado
- WampServer (con MySQL) ejecutándose
- MySQL accesible en `localhost:3306`

### 6.2 Instalación

#### Paso 1: Clonar o descargar el proyecto

```bash
# El proyecto debería estar en:
C:\Users\[Tu Usuario]\Desktop\API_EVAL3
```

#### Paso 2: Instalar dependencias

```bash
cd C:\Users\[Tu Usuario]\Desktop\API_EVAL3

# Crear un entorno virtual (opcional pero recomendado)
python -m venv venv
venv\Scripts\activate

# Instalar paquetes requeridos
pip install -r requirements.txt
```

#### Paso 3: Crear la base de datos

1. Abrir phpMyAdmin (acceder a `localhost/phpmyadmin`)
2. Crear una nueva base de datos (o usar una existente)
3. Importar el archivo `datos/ddl.sql`:
   - En phpMyAdmin, ir a "Importar"
   - Seleccionar `datos/ddl.sql`
   - Hacer clic en "Ejecutar"

Alternativa por consola MySQL:

```bash
mysql -u root < datos/ddl.sql
```

#### Paso 4: Configurar parámetros (si es necesario)

Editar `app/config/settings.py` si los datos de conexión son diferentes:

```python
DB_HOST = "localhost"    # Host del servidor MySQL
DB_USER = "root"         # Usuario MySQL
DB_PASSWORD = ""         # Contraseña (vacío para WAMP default)
DB_NAME = "api_eval3"    # Nombre de la base de datos
```

#### Paso 5: Ejecutar el programa

```bash
python -m app.main
```

O desde la carpeta del proyecto:

```bash
cd C:\Users\[Tu Usuario]\Desktop\API_EVAL3
python -m app.main
```

### 6.3 Salida esperada

```
============================================================
  INICIANDO SISTEMA API_EVAL3
============================================================

1. Creando cliente de JSONPlaceholder...
   ✓ Cliente creado

2. Creando conexión a MySQL...
   ✓ Conexión exitosa

3. Creando servicios...
   ✓ Servicios creados

============================================================
  FASE 1: IMPORTAR USUARIOS DESDE JSONPLACEHOLDER
============================================================

Ejecutando: UsuarioService.importar_desde_api()
...

✓ SISTEMA FUNCIONANDO CORRECTAMENTE
```

---

## 7. Estructura de la Base de Datos

### Tabla: usuario

| Campo | Tipo | Restricciones | Propósito |
|-------|------|---|----------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único |
| `nombre` | VARCHAR(255) | NOT NULL | Nombre del usuario |
| `correo` | VARCHAR(255) | UNIQUE, NOT NULL | Email (único) |
| `creado_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Timestamp de creación |

### Tabla: post

| Campo | Tipo | Restricciones | Propósito |
|-------|------|---|----------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único |
| `usuario_id` | INT | FOREIGN KEY, NOT NULL | Referencia a usuario |
| `titulo` | VARCHAR(255) | NOT NULL | Título del post |
| `contenido` | TEXT | NOT NULL | Cuerpo del post |
| `creado_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Timestamp de creación |

**Relación**: Cada post pertenece a un usuario. Si se elimina un usuario, sus posts se eliminan automáticamente (`ON DELETE CASCADE`).

---

## 8. Clases Principales

### JsonPlaceholderClient

Encapsula la comunicación con la API JSONPlaceholder.

**Métodos públicos:**
- `get_usuarios()` → Lista[Dict]
- `get_posts()` → Lista[Dict]

### Usuario

Modelo de dominio para usuarios.

**Atributos:**
- `id`: int
- `nombre`: str
- `correo`: str

**Métodos:**
- `__init__(id, nombre, correo)`
- `from_dict(data)` (classmethod)
- `__repr__()` (para depuración)

### UsuarioService

Servicio que coordina operaciones con usuarios.

**Métodos públicos:**
- `importar_desde_api()` → bool
- `listar()` → Lista[Usuario]
- `eliminar_por_id(id)` → bool

### Conexion

Gestiona la conexión a MySQL.

**Métodos públicos:**
- `conectar()` → bool
- `obtener_conexion()` → MySQLConnection
- `cerrar()` → bool

---

## 9. Conclusión Académica

### Lo aprendido en este proyecto:

1. **Arquitectura en capas**: Cómo separar responsabilidades en un proyecto real
2. **POO en la práctica**: Uso de clases, herencia, métodos de clase y encapsulación
3. **Consumo de APIs**: Cómo integrar servicios externos en una aplicación
4. **Persistencia de datos**: Operaciones CRUD en bases de datos relacionales
5. **Inyección de dependencias**: Patrón fundamental para código mantenible

### Relevancia en el mundo real:

Este proyecto simula el funcionamiento de aplicaciones **backend** reales:

- Las APIs públicas son consumidas constantemente por aplicaciones web
- La persistencia en bases de datos es esencial para cualquier servicio
- La arquitectura en capas es estándar en la industria
- Los conceptos de POO son transferibles a cualquier lenguaje (Java, C#, etc.)

### Mejoras futuras (para ampliar el aprendizaje):

- Agregar autenticación JWT
- Implementar caché de datos
- Crear endpoints REST propios (con Flask/FastAPI)
- Agregar pruebas unitarias (unittest, pytest)
- Usar ORM (SQLAlchemy) en lugar de SQL directo
- Implementar logging estructurado

---

## 10. Autor y Contexto

**Asignatura**: Programación Orientada a Objetos  
**Evaluación**: Unidad 3 - Integración de Sistemas  
**Tecnologías**: Python, MySQL, API REST  
**Desarrollado con**: GitHub Copilot, Visual Studio Code, Python 3.8+

---

## 11. Referencias

- [JSONPlaceholder - API pública de pruebas](https://jsonplaceholder.typicode.com/)
- [Documentación oficial de Python](https://docs.python.org/3/)
- [MySQL 5.7 - Documentación](https://dev.mysql.com/doc/refman/5.7/en/)
- [WampServer - Descargas](https://www.wampserver.com/)
- [Principios SOLID](https://en.wikipedia.org/wiki/SOLID)

---

**Última actualización**: Diciembre 2025  
**Estado**: Proyecto completado y listo para evaluación


