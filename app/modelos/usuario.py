"""
Módulo de modelo para la clase Usuario.

Este módulo define la clase Usuario que representa la estructura
de datos de un usuario en el sistema.
"""

from typing import Dict, Any


class Usuario:
    """
    Clase modelo que representa un usuario del sistema.
    
    Encapsula los atributos principales de un usuario y proporciona
    métodos para inicialización y conversión de datos.
    
    Attributes:
        id (int): Identificador único del usuario.
        nombre (str): Nombre completo del usuario.
        correo (str): Dirección de correo electrónico del usuario.
    """
    
    def __init__(self, id: int, nombre: str, correo: str) -> None:
        """
        Constructor de la clase Usuario.
        
        Inicializa una instancia de Usuario con los atributos proporcionados.
        
        Args:
            id (int): Identificador único del usuario.
            nombre (str): Nombre completo del usuario.
            correo (str): Dirección de correo electrónico del usuario.
        """
        self.id = id
        self.nombre = nombre
        self.correo = correo
    
    def __repr__(self) -> str:
        """
        Retorna una representación legible de la instancia de Usuario.
        
        Útil para depuración y visualización de objetos en la consola.
        
        Returns:
            str: Representación en formato Usuario(id, nombre, correo).
        """
        return f"Usuario(id={self.id}, nombre='{self.nombre}', correo='{self.correo}')"
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Usuario':
        """
        Crea una instancia de Usuario a partir de un diccionario.
        
        Método de clase (classmethod) que permite construir un objeto Usuario
        desde datos en formato diccionario, típicamente provenientes de una
        respuesta JSON de la API.
        
        Args:
            data (Dict[str, Any]): Diccionario con los datos del usuario.
                Debe contener al menos las claves 'id', 'name' y 'email'.
        
        Returns:
            Usuario: Nueva instancia de Usuario con los datos del diccionario.
            
        Raises:
            KeyError: Si faltan claves requeridas en el diccionario.
        """
        return cls(
            id=data['id'],
            nombre=data['name'],
            correo=data['email']
        )
