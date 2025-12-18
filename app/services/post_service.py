"""
Módulo servicio para gestionar operaciones relacionadas con posts.

Este módulo proporciona la clase PostService que actúa como intermediaria
entre la API JSONPlaceholder, los modelos de Post y la base de datos MySQL,
coordinando la obtención, conversión y almacenamiento de datos de posts.
"""

from typing import List
from mysql.connector import Error
from app.api.jsonplaceholder_client import JsonPlaceholderClient
from app.modelos.post import Post
from app.config.conexion import Conexion


class PostService:
    """
    Servicio para coordinar operaciones con posts.
    
    Esta clase actúa como intermediaria entre el cliente HTTP (JsonPlaceholderClient),
    el modelo de dominio (Post) y la base de datos MySQL, proporcionando métodos
    de alto nivel para obtener, convertir, importar, listar y eliminar posts.
    
    Attributes:
        cliente (JsonPlaceholderClient): Cliente para acceder a la API JSONPlaceholder.
        conexion (Conexion): Objeto para gestionar la conexión a MySQL.
    """
    
    def __init__(self, cliente: JsonPlaceholderClient, conexion: Conexion) -> None:
        """
        Constructor de la clase PostService.
        
        Inicializa el servicio con un cliente JSON Placeholder y una conexión
        a la base de datos que se utilizarán para obtener y guardar datos.
        
        Args:
            cliente (JsonPlaceholderClient): Instancia del cliente para la API.
            conexion (Conexion): Instancia de la conexión a MySQL.
        """
        self.cliente = cliente
        self.conexion = conexion
    
    def _obtener_posts_api(self) -> List[Post]:
        """
        Obtiene la lista de posts desde la API y la convierte a objetos Post.
        
        Método privado que realiza una solicitud a través del cliente para obtener
        los datos de posts desde JSONPlaceholder, y luego convierte cada
        diccionario en un objeto Post utilizando el método from_dict.
        
        Returns:
            List[Post]: Lista de objetos Post obtenidos de la API.
                Si la API retorna una lista vacía o hay un error, retorna una lista vacía.
        """
        try:
            # Obtener datos de posts desde la API
            datos_posts = self.cliente.get_posts()
            
            # Convertir cada diccionario en un objeto Post
            posts = [Post.from_dict(dato) for dato in datos_posts]
            
            return posts
            
        except KeyError as e:
            # Manejar caso donde faltan claves esperadas en los datos
            print(f"Error: Estructura de datos incompleta - {str(e)}")
            return []
            
        except Exception as e:
            # Manejar errores inesperados
            print(f"Error al obtener posts de la API: {str(e)}")
            return []
    
    def importar_desde_api(self) -> bool:
        """
        Importa posts desde la API JSONPlaceholder y los guarda en la base de datos.
        
        Obtiene la lista de posts desde la API, convierte cada uno a un objeto Post,
        y luego intenta guardar cada post en la base de datos MySQL, asociándolo
        con su usuario correspondiente.
        
        Returns:
            bool: True si la importación fue exitosa, False si ocurrió un error.
        """
        try:
            # Obtener posts desde la API
            posts = self._obtener_posts_api()
            
            if not posts:
                print("No se obtuvieron posts de la API.")
                return False
            
            # Obtener la conexión a la base de datos
            conexion = self.conexion.obtener_conexion()
            
            if conexion is None:
                print("Error: No se pudo obtener la conexión a la base de datos.")
                return False
            
            # Crear un cursor para ejecutar las consultas
            cursor = conexion.cursor()
            
            # SQL para insertar un post (asume que existe en ddl.sql)
            sql_insertar = """
                INSERT INTO post (id, usuario_id, titulo, contenido)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE titulo=VALUES(titulo), contenido=VALUES(contenido)
            """
            
            posts_insertados = 0
            
            # Insertar cada post en la base de datos
            for post in posts:
                try:
                    cursor.execute(sql_insertar, (
                        post.id, 
                        post.user_id, 
                        post.titulo, 
                        post.contenido
                    ))
                    posts_insertados += 1
                except Error as e:
                    print(f"Error al insertar post {post.id}: {str(e)}")
            
            # Confirmar las inserciones (commit)
            conexion.commit()
            
            print(f"Importación completada: {posts_insertados} post(s) importado(s).")
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
    
    def listar(self) -> List[Post]:
        """
        Lista todos los posts almacenados en la base de datos.
        
        Realiza una consulta a la base de datos para obtener todos los posts
        y los convierte a objetos Post.
        
        Returns:
            List[Post]: Lista de objetos Post almacenados en la BD.
                Retorna lista vacía si no hay posts o si ocurre un error.
        """
        try:
            # Obtener la conexión a la base de datos
            conexion = self.conexion.obtener_conexion()
            
            if conexion is None:
                print("Error: No se pudo obtener la conexión a la base de datos.")
                return []
            
            # Crear un cursor para ejecutar la consulta
            cursor = conexion.cursor(dictionary=True)
            
            # SQL para obtener todos los posts (asume que existe en ddl.sql)
            sql_listar = "SELECT id, usuario_id, titulo, contenido FROM post"
            
            cursor.execute(sql_listar)
            
            # Obtener todos los resultados
            resultados = cursor.fetchall()
            
            # Convertir cada fila a un objeto Post
            posts = []
            for fila in resultados:
                # Mapear las claves de la BD a los parámetros de from_dict
                datos = {
                    'id': fila.get('id'),
                    'userId': fila.get('usuario_id'),
                    'title': fila.get('titulo'),
                    'body': fila.get('contenido')
                }
                post = Post.from_dict(datos)
                posts.append(post)
            
            cursor.close()
            
            return posts
            
        except Error as e:
            # Capturar errores de MySQL
            print(f"Error de base de datos: {str(e)}")
            return []
            
        except Exception as e:
            # Capturar otros errores inesperados
            print(f"Error al listar posts: {str(e)}")
            return []
    
    def eliminar_por_id(self, id: int) -> bool:
        """
        Elimina un post de la base de datos por su identificador.
        
        Busca y elimina el post con el ID especificado de la base de datos.
        
        Args:
            id (int): Identificador único del post a eliminar.
        
        Returns:
            bool: True si el post fue eliminado correctamente, False si ocurrió un error.
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
            
            # SQL para eliminar un post (asume que existe en ddl.sql)
            sql_eliminar = "DELETE FROM post WHERE id = %s"
            
            cursor.execute(sql_eliminar, (id,))
            
            # Obtener el número de filas afectadas
            filas_afectadas = cursor.rowcount
            
            # Confirmar la eliminación (commit)
            conexion.commit()
            
            cursor.close()
            
            if filas_afectadas > 0:
                print(f"Post con ID {id} eliminado correctamente.")
                return True
            else:
                print(f"No se encontró post con ID {id}.")
                return False
                
        except Error as e:
            # Capturar errores de MySQL
            print(f"Error de base de datos: {str(e)}")
            return False
            
        except Exception as e:
            # Capturar otros errores inesperados
            print(f"Error al eliminar post: {str(e)}")
            return False
