# API_EVAL3 — Programación Orientada a Objetos

## Evaluación Unidad 3  
### Consumo de API REST, Arquitectura en Capas, Persistencia en MySQL y Encriptación  
**Asignatura:** Programación Orientada a Objetos  
**Lenguaje:** Python  

---

## 1. Descripción General del Proyecto

**API_EVAL3** es un proyecto académico desarrollado para la Evaluación de la Unidad 3 de Programación Orientada a Objetos.  
El objetivo principal del proyecto es **demostrar la aplicación práctica de los conceptos de POO** mediante el consumo de una **API REST externa**, el procesamiento de los datos utilizando **arquitectura en capas**, y la **persistencia de información en una base de datos MySQL**.

El sistema consume datos desde la API pública **JSONPlaceholder**, los transforma en objetos de dominio, los almacena en una base de datos local y permite interactuar con ellos mediante un **menú por consola**, simulando el funcionamiento de un sistema backend real.

Además, el proyecto incorpora una **capa de negocio** que demuestra el uso de **encriptación de cadenas** mediante el algoritmo SHA-256, cumpliendo con los criterios solicitados en la pauta de evaluación.

---

## 2. Objetivos Académicos

Este proyecto tiene como objetivos:

- Aplicar Programación Orientada a Objetos en un contexto real
- Diseñar una arquitectura en capas clara y mantenible
- Consumir y procesar datos desde una API REST externa
- Persistir datos en una base de datos relacional MySQL
- Implementar separación de responsabilidades
- Demostrar encriptación de cadenas en la capa de negocio
- Utilizar un menú interactivo para ejecutar funcionalidades del sistema
- Desarrollar el proyecto utilizando herramientas profesionales como GitHub Copilot

---

## 3. Arquitectura del Proyecto

El proyecto está estructurado siguiendo una **arquitectura en capas**, similar a la utilizada en sistemas backend reales.

API_EVAL3
├── app/
│ ├── api/ # Capa de integración con API externa
│ │ └── jsonplaceholder_client.py
│ │
│ ├── modelos/ # Capa de modelos de dominio (POO)
│ │ ├── usuario.py
│ │ └── post.py
│ │
│ ├── services/ # Capa de servicios / aplicación
│ │ ├── usuario_service.py
│ │ └── post_service.py
│ │
│ ├── negocio/ # Capa de negocio
│ │ └── encriptador.py
│ │
│ ├── config/ # Configuración y conexión a BD
│ │ ├── conexion.py
│ │ └── settings.py
│ │
│ └── main.py # Punto de entrada y menú principal
│
├── datos/
│ └── ddl.sql # Script de creación de base de datos
│
├── requirements.txt # Dependencias del proyecto
└── README.md # Documentación académica

yaml
Copiar código

---

## 4. Relación con Programación Orientada a Objetos

| Capa | Concepto POO | Función |
|----|----|----|
| modelos | Clases y objetos | Representan entidades del dominio |
| services | Métodos, composición | Coordinan la lógica del sistema |
| negocio | Encapsulación | Procesamiento interno (encriptación) |
| api | Abstracción | Aísla la comunicación HTTP |
| config | Manejo de recursos | Controla la conexión a la BD |
| main | Orquestación | Coordina el flujo general |

---

## 5. Tecnologías Utilizadas

- **Python 3.8+**
- **MySQL** (mediante WampServer)
- **JSONPlaceholder** (API REST pública)
- **requests** (cliente HTTP)
- **mysql-connector-python**
- **Visual Studio Code**

---

## 6. Conceptos de POO Aplicados

### 6.1 Clases y Objetos

Las entidades principales del sistema están representadas mediante clases:

```python
class Usuario:
    def __init__(self, id, nombre, correo):
        self.id = id
        self.nombre = nombre
        self.correo = correo
Cada instancia representa un objeto independiente dentro del sistema.

6.2 Métodos de Clase
Se utilizan métodos de clase para crear objetos a partir de estructuras JSON:

python
Copiar código
@classmethod
def from_dict(cls, data):
    return cls(
        id=data['id'],
        nombre=data['name'],
        correo=data['email']
    )
6.3 Encapsulación
Los detalles internos de implementación se mantienen ocultos, exponiendo únicamente métodos públicos necesarios para el funcionamiento del sistema.

6.4 Separación de Responsabilidades
Cada clase y módulo cumple una única responsabilidad, evitando dependencias innecesarias entre capas.

7. Capa de Negocio: Encriptación
La carpeta negocio representa la capa de negocio del sistema.

Encriptador
El archivo encriptador.py implementa una clase Encriptador que utiliza el algoritmo SHA-256 mediante la librería estándar hashlib.

Funciones principales:

Encriptar cadenas de texto

Verificar si un texto coincide con un hash

Demostrar procesamiento de datos independiente de la API y la BD

Esta funcionalidad se ejecuta y demuestra directamente desde el menú principal del sistema.

8. Flujo General del Sistema
Flujo completo:
css
Copiar código
Usuario
  ↓
Menú principal (main.py)
  ↓
Servicios
  ↓
Cliente API / Base de Datos
  ↓
Modelos
9. Menú Interactivo
El sistema se ejecuta mediante un menú por consola que permite:

Ejecutar prueba integrada completa

Importar usuarios desde la API

Importar posts desde la API

Listar usuarios desde la base de datos

Listar posts desde la base de datos

Eliminar usuarios

Eliminar posts

Probar la encriptación (capa de negocio)

Salir

Este menú permite demostrar el funcionamiento completo del sistema de forma controlada.

10. Prueba Integrada del Sistema
El sistema incluye una prueba integrada que ejecuta todas las capas:

Consumo de API REST

Conversión de datos a objetos

Persistencia en MySQL

Recuperación desde base de datos

Visualización por consola

Esto permite validar que la arquitectura funciona correctamente como un todo.

11. Base de Datos
Tabla usuario
Campo	Tipo	Descripción
id	INT	Identificador único
nombre	VARCHAR	Nombre del usuario
correo	VARCHAR	Email único

Tabla post
Campo	Tipo	Descripción
id	INT	Identificador
usuario_id	INT	Relación con usuario
titulo	VARCHAR	Título
contenido	TEXT	Contenido

12. Instrucciones de Ejecución
Requisitos
Python 3.8+

WampServer activo

MySQL en localhost

Pasos
bash
Copiar código
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
Crear la base de datos importando:

bash
Copiar código
datos/ddl.sql
Ejecutar el sistema:

bash
Copiar código
python -m app.main
13. Conclusión Académica
Este proyecto demuestra:

Aplicación práctica de Programación Orientada a Objetos

Uso de arquitectura en capas

Consumo de APIs REST

Persistencia en bases de datos

Separación de responsabilidades

Uso de una capa de negocio con encriptación

El proyecto simula el comportamiento de aplicaciones backend reales y cumple con los criterios establecidos en la evaluación.

14. Autor y Contexto
Evaluación: Unidad 3 – Programación Orientada a Objetos
Desarrollado por: Nicolás Cárdenas
Herramientas: Python, MySQL, GitHub Copilot, VS Code

Estado: Proyecto funcional, probado y listo para evaluación