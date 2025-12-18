"""
Módulo servicio para gestionar operaciones relacionadas con usuarios.

Este módulo proporciona la clase UsuarioService que actúa como intermediaria
entre la API JSONPlaceholder, los modelos de Usuario y la base de datos MySQL,
coordinando la obtención, conversión y almacenamiento de datos de usuarios.
"""

from typing import List
from mysql.connector import Error
from app.api.jsonplaceholder_client import JsonPlaceholderClient
from app.modelos.usuario import Usuario
from app.config.conexion import Conexion


class UsuarioService:
    """
    Servicio para coordinar operaciones con usuarios.
    
    Esta clase actúa como intermediaria entre el cliente HTTP (JsonPlaceholderClient),
    el modelo de dominio (Usuario) y la base de datos MySQL, proporcionando métodos
    de alto nivel para obtener, convertir, importar, listar y eliminar usuarios.
    
    Attributes:
        cliente (JsonPlaceholderClient): Cliente para acceder a la API JSONPlaceholder.
        conexion (Conexion): Objeto para gestionar la conexión a MySQL.
    """
    
    def __init__(self, cliente: JsonPlaceholderClient, conexion: Conexion) -> None:
        """
        Constructor de la clase UsuarioService.
        
        Inicializa el servicio con un cliente JSON Placeholder y una conexión
        a la base de datos que se utilizarán para obtener y guardar datos.
        
        Args:
            cliente (JsonPlaceholderClient): Instancia del cliente para la API.
            conexion (Conexion): Instancia de la conexión a MySQL.
        """
        self.cliente = cliente
        self.conexion = conexion
    
    def _obtener_usuarios_api(self) -> List[Usuario]:
        """
        Obtiene la lista de usuarios desde la API y la convierte a objetos Usuario.
        
        Método privado que realiza una solicitud a través del cliente para obtener
        los datos de usuarios desde JSONPlaceholder, y luego convierte cada
        diccionario en un objeto Usuario utilizando el método from_dict.
        
        Returns:
            List[Usuario]: Lista de objetos Usuario obtenidos de la API.
                Si la API retorna una lista vacía o hay un error, retorna una lista vacía.
        """
        try:
            # Obtener datos de usuarios desde la API
            datos_usuarios = self.cliente.get_usuarios()
            
            # Convertir cada diccionario en un objeto Usuario
            usuarios = [Usuario.from_dict(dato) for dato in datos_usuarios]
            
            return usuarios
            
        except KeyError as e:
            # Manejar caso donde faltan claves esperadas en los datos
            print(f"Error: Estructura de datos incompleta - {str(e)}")
            return []
            
        except Exception as e:
            # Manejar errores inesperados
            print(f"Error al obtener usuarios de la API: {str(e)}")
            return []
    
    def importar_desde_api(self) -> bool:
        """
        Importa usuarios desde la API JSONPlaceholder y los guarda en la base de datos.
        
        Obtiene la lista de usuarios desde la API, convierte cada uno a un objeto Usuario,
        y luego intenta guardar cada usuario en la base de datos MySQL.
        
        Returns:
            bool: True si la importación fue exitosa, False si ocurrió un error.
        """
        try:
            # Obtener usuarios desde la API
            usuarios = self._obtener_usuarios_api()
            
            if not usuarios:
                print("No se obtuvieron usuarios de la API.")
                return False
            
            # Obtener la conexión a la base de datos
            conexion = self.conexion.obtener_conexion()
            
            if conexion is None:
                print("Error: No se pudo obtener la conexión a la base de datos.")
                return False
            
            # Crear un cursor para ejecutar las consultas
            cursor = conexion.cursor()
            
            # SQL para insertar un usuario (asume que existe en ddl.sql)
            sql_insertar = """
                INSERT INTO usuario (id, nombre, correo)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE nombre=VALUES(nombre), correo=VALUES(correo)
            """
            
            usuarios_insertados = 0
            
            # Insertar cada usuario en la base de datos
            for usuario in usuarios:
                try:
                    cursor.execute(sql_insertar, (usuario.id, usuario.nombre, usuario.correo))
                    usuarios_insertados += 1
                except Error as e:
                    print(f"Error al insertar usuario {usuario.id}: {str(e)}")
            
            # Confirmar las inserciones (commit)
            conexion.commit()
            
            print(f"Importación completada: {usuarios_insertados} usuario(s) importado(s).")
            cursor.close()
            
            return True
            
        except Error as e:
            # Capturar errores de MySQL
            print(f"Error de base de datos: {str(e)}")
            return False
            
        except Exception as e:
            # Capturar otros errores inesperados
            print(f"Error durante la importación: {str(e)}")
            return False
    
    def listar(self) -> List[Usuario]:
        """
        Lista todos los usuarios almacenados en la base de datos.
        
        Realiza una consulta a la base de datos para obtener todos los usuarios
        y los convierte a objetos Usuario.
        
        Returns:
            List[Usuario]: Lista de objetos Usuario almacenados en la BD.
                Retorna lista vacía si no hay usuarios o si ocurre un error.
        """
        try:
            # Obtener la conexión a la base de datos
            conexion = self.conexion.obtener_conexion()
            
            if conexion is None:
                print("Error: No se pudo obtener la conexión a la base de datos.")
                return []
            
            # Crear un cursor para ejecutar la consulta
            cursor = conexion.cursor(dictionary=True)
            
            # SQL para obtener todos los usuarios (asume que existe en ddl.sql)
            sql_listar = "SELECT id, nombre, correo FROM usuario"
            
            cursor.execute(sql_listar)
            
            # Obtener todos los resultados
            resultados = cursor.fetchall()
            
            # Convertir cada fila a un objeto Usuario
            usuarios = []
            for fila in resultados:
                usuario = Usuario.from_dict(dict(fila))
                usuarios.append(usuario)
            
            cursor.close()
            
            return usuarios
            
        except Error as e:
            # Capturar errores de MySQL
            print(f"Error de base de datos: {str(e)}")
            return []
            
        except Exception as e:
            # Capturar otros errores inesperados
            print(f"Error al listar usuarios: {str(e)}")
            return []
    
    def eliminar_por_id(self, id: int) -> bool:
        """
        Elimina un usuario de la base de datos por su identificador.
        
        Busca y elimina el usuario con el ID especificado de la base de datos.
        
        Args:
            id (int): Identificador único del usuario a eliminar.
        
        Returns:
            bool: True si el usuario fue eliminado correctamente, False si ocurrió un error.
        """
        try:
            # Validar que el ID sea válido
            if not isinstance(id, int) or id <= 0:
                print("Error: El ID debe ser un número entero positivo.")
                return False
            
            # Obtener la conexión a la base de datos
            conexion = self.conexion.obtener_conexion()
            
            if conexion is None:
                print("Error: No se pudo obtener la conexión a la base de datos.")
                return False
            
            # Crear un cursor para ejecutar la consulta
            cursor = conexion.cursor()
            
            # SQL para eliminar un usuario (asume que existe en ddl.sql)
            sql_eliminar = "DELETE FROM usuario WHERE id = %s"
            
            cursor.execute(sql_eliminar, (id,))
            
            # Obtener el número de filas afectadas
            filas_afectadas = cursor.rowcount
            
            # Confirmar la eliminación (commit)
            conexion.commit()
            
            cursor.close()
            
            if filas_afectadas > 0:
                print(f"Usuario con ID {id} eliminado correctamente.")
                return True
            else:
                print(f"No se encontró usuario con ID {id}.")
                return False
                
        except Error as e:
            # Capturar errores de MySQL
            print(f"Error de base de datos: {str(e)}")
            return False
            
        except Exception as e:
            # Capturar otros errores inesperados
            print(f"Error al eliminar usuario: {str(e)}")
            return False
