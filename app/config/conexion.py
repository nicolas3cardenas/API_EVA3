"""
Módulo para gestionar la conexión a la base de datos MySQL.

Este módulo proporciona la clase Conexion que encapsula toda la lógica
necesaria para establecer, mantener y cerrar una conexión con la base
de datos MySQL del proyecto.
"""

import mysql.connector
from mysql.connector import Error
from app.config.settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME


class Conexion:
    """
    Clase para gestionar la conexión a la base de datos MySQL.
    
    Esta clase encapsula la lógica de conexión a MySQL, permitiendo
    establecer, obtener y cerrar conexiones de forma segura y ordenada.
    Implementa un patrón singleton para evitar múltiples conexiones.
    
    Attributes:
        _conexion (mysql.connector.MySQLConnection): Objeto de conexión a MySQL.
        _host (str): Host del servidor MySQL.
        _usuario (str): Usuario para autenticación.
        _password (str): Contraseña para autenticación.
        _base_datos (str): Nombre de la base de datos.
    """
    
    def __init__(self) -> None:
        """
        Constructor de la clase Conexion.
        
        Inicializa los atributos de conexión con los valores obtenidos
        de las variables de configuración en settings.py.
        No realiza la conexión inmediatamente (lazy initialization).
        """
        self._conexion = None
        self._host = DB_HOST
        self._usuario = DB_USER
        self._password = DB_PASSWORD
        self._base_datos = DB_NAME
    
    def conectar(self) -> bool:
        """
        Establece la conexión con la base de datos MySQL.
        
        Intenta conectar al servidor MySQL utilizando los parámetros
        configurados. Si ya existe una conexión activa, no intenta
        conectar nuevamente.
        
        Returns:
            bool: True si la conexión se estableció correctamente,
                  False si ocurrió un error.
        """
        try:
            # Verificar si ya existe una conexión activa
            if self._conexion is not None and self._conexion.is_connected():
                print("Ya existe una conexión activa.")
                return True
            
            # Crear la conexión con los parámetros configurados
            self._conexion = mysql.connector.connect(
                host=self._host,
                user=self._usuario,
                password=self._password,
                database=self._base_datos
            )
            
            # Verificar que la conexión fue exitosa
            if self._conexion.is_connected():
                print(f"Conexión exitosa a {self._base_datos} en {self._host}")
                return True
            else:
                print("Error: No se pudo verificar la conexión.")
                return False
                
        except Error as e:
            # Capturar errores específicos de MySQL
            print(f"Error de conexión MySQL: {str(e)}")
            self._conexion = None
            return False
            
        except Exception as e:
            # Capturar otros errores inesperados
            print(f"Error inesperado: {str(e)}")
            self._conexion = None
            return False
    
    def obtener_conexion(self):
        """
        Obtiene la conexión activa a la base de datos.
        
        Si no existe una conexión activa, intenta establecerla.
        Este método permite reutilizar la misma conexión en diferentes
        partes del código.
        
        Returns:
            mysql.connector.MySQLConnection: Objeto de conexión activo.
                Retorna None si la conexión no pudo establecerse.
        """
        try:
            # Si no hay conexión o no está activa, intentar conectar
            if self._conexion is None or not self._conexion.is_connected():
                self.conectar()
            
            return self._conexion
            
        except Exception as e:
            # Capturar errores inesperados
            print(f"Error al obtener conexión: {str(e)}")
            return None
    
    def cerrar(self) -> bool:
        """
        Cierra la conexión con la base de datos de forma segura.
        
        Termina la conexión activa con MySQL si existe. Es importante
        llamar a este método al finalizar el programa para liberar recursos.
        
        Returns:
            bool: True si la conexión se cerró correctamente,
                  False si ocurrió un error o no había conexión.
        """
        try:
            # Verificar si existe una conexión activa
            if self._conexion is not None and self._conexion.is_connected():
                self._conexion.close()
                print(f"Conexión a {self._base_datos} cerrada correctamente.")
                return True
            else:
                print("No hay conexión activa para cerrar.")
                return False
                
        except Error as e:
            # Capturar errores específicos de MySQL
            print(f"Error al cerrar la conexión: {str(e)}")
            return False
            
        except Exception as e:
            # Capturar otros errores inesperados
            print(f"Error inesperado al cerrar: {str(e)}")
            return False
        
        finally:
            # Asegurar que el atributo se establezca en None
            self._conexion = None
