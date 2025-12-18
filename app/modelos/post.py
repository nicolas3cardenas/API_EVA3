"""
Módulo de modelo para la clase Post.

Este módulo define la clase Post que representa la estructura
de datos de una publicación en el sistema.
"""

from typing import Dict, Any


class Post:
    """
    Clase modelo que representa una publicación del sistema.
    
    Encapsula los atributos principales de un post y proporciona
    métodos para inicialización y conversión de datos.
    
    Attributes:
        id (int): Identificador único del post.
        user_id (int): Identificador del usuario propietario del post.
        titulo (str): Título o asunto del post.
        contenido (str): Contenido o cuerpo del post.
    """
    
    def __init__(self, id: int, user_id: int, titulo: str, contenido: str) -> None:
        """
        Constructor de la clase Post.
        
        Inicializa una instancia de Post con los atributos proporcionados.
        
        Args:
            id (int): Identificador único del post.
            user_id (int): Identificador del usuario propietario del post.
            titulo (str): Título o asunto del post.
            contenido (str): Contenido o cuerpo del post.
        """
        self.id = id
        self.user_id = user_id
        self.titulo = titulo
        self.contenido = contenido
    
    def __repr__(self) -> str:
        """
        Retorna una representación legible de la instancia de Post.
        
        Útil para depuración y visualización de objetos en la consola.
        
        Returns:
            str: Representación en formato Post(id, user_id, titulo...).
        """
        return f"Post(id={self.id}, user_id={self.user_id}, titulo='{self.titulo[:30]}...')"
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Post':
        """
        Crea una instancia de Post a partir de un diccionario.
        
        Método de clase (classmethod) que permite construir un objeto Post
        desde datos en formato diccionario, típicamente provenientes de una
        respuesta JSON de la API.
        
        Args:
            data (Dict[str, Any]): Diccionario con los datos del post.
                Debe contener al menos las claves 'id', 'userId', 'title' y 'body'.
        
        Returns:
            Post: Nueva instancia de Post con los datos del diccionario.
            
        Raises:
            KeyError: Si faltan claves requeridas en el diccionario.
        """
        return cls(
            id=data['id'],
            user_id=data['userId'],
            titulo=data['title'],
            contenido=data['body']
        )
