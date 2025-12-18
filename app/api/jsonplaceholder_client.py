"""
Módulo cliente para consumir la API pública JSONPlaceholder.

Este módulo proporciona una clase que actúa como cliente HTTP para
interactuar con los endpoints de la API JSONPlaceholder, permitiendo
obtener datos de usuarios y posts.
"""

import requests
from typing import List, Dict, Any


class JsonPlaceholderClient:
    """
    Cliente para consumir la API pública de JSONPlaceholder.
    
    Esta clase encapsula la lógica necesaria para realizar solicitudes HTTP
    a la API JSONPlaceholder y procesar las respuestas obtenidas.
    
    Attributes:
        BASE_URL (str): URL base de la API JSONPlaceholder.
    """
    
    # Constante que define la URL base de la API
    BASE_URL = "https://jsonplaceholder.typicode.com"
    
    # Timeout en segundos para las solicitudes HTTP
    TIMEOUT = 10
    
    def get_usuarios(self) -> List[Dict[str, Any]]:
        """
        Obtiene la lista de usuarios desde la API JSONPlaceholder.
        
        Realiza una solicitud GET al endpoint /users y retorna los datos
        de los usuarios en formato de lista de diccionarios.
        
        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con datos de usuarios.
                Si la solicitud falla, retorna una lista vacía.
                
        Raises:
            requests.exceptions.RequestException: Se captura internamente
                para manejar errores de conexión.
        """
        try:
            # Construir la URL del endpoint
            url = f"{self.BASE_URL}/users"
            
            # Realizar la solicitud GET
            respuesta = requests.get(url, timeout=self.TIMEOUT)
            
            # Validar que la respuesta sea exitosa (código 200)
            respuesta.raise_for_status()
            
            # Retornar los datos en formato JSON
            return respuesta.json()
            
        except requests.exceptions.Timeout:
            print("Error: Tiempo de espera agotado al conectar con la API.")
            return []
            
        except requests.exceptions.ConnectionError:
            print("Error: No se pudo conectar con la API JSONPlaceholder.")
            return []
            
        except requests.exceptions.HTTPError as e:
            print(f"Error HTTP: {e.response.status_code} - {e.response.reason}")
            return []
            
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {str(e)}")
            return []
            
        except ValueError as e:
            print(f"Error al procesar la respuesta JSON: {str(e)}")
            return []
    
    def get_posts(self) -> List[Dict[str, Any]]:
        """
        Obtiene la lista de posts desde la API JSONPlaceholder.
        
        Realiza una solicitud GET al endpoint /posts y retorna los datos
        de los posts en formato de lista de diccionarios.
        
        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con datos de posts.
                Si la solicitud falla, retorna una lista vacía.
                
        Raises:
            requests.exceptions.RequestException: Se captura internamente
                para manejar errores de conexión.
        """
        try:
            # Construir la URL del endpoint
            url = f"{self.BASE_URL}/posts"
            
            # Realizar la solicitud GET
            respuesta = requests.get(url, timeout=self.TIMEOUT)
            
            # Validar que la respuesta sea exitosa (código 200)
            respuesta.raise_for_status()
            
            # Retornar los datos en formato JSON
            return respuesta.json()
            
        except requests.exceptions.Timeout:
            print("Error: Tiempo de espera agotado al conectar con la API.")
            return []
            
        except requests.exceptions.ConnectionError:
            print("Error: No se pudo conectar con la API JSONPlaceholder.")
            return []
            
        except requests.exceptions.HTTPError as e:
            print(f"Error HTTP: {e.response.status_code} - {e.response.reason}")
            return []
            
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {str(e)}")
            return []
            
        except ValueError as e:
            print(f"Error al procesar la respuesta JSON: {str(e)}")
            return []
