"""
Módulo de encriptación - Capa de negocio.

Este módulo proporciona funcionalidades de encriptación utilizando
el algoritmo SHA-256, demostrando la capa de lógica de negocio en
una arquitectura estratificada de Programación Orientada a Objetos.
"""

import hashlib


class Encriptador:
    """
    Clase para encriptar y verificar datos utilizando SHA-256.
    
    Implementa métodos de encriptación mediante hashing criptográfico,
    sin depender de librerías externas. Demuestra el uso de hashlib
    de la librería estándar de Python.
    
    El algoritmo SHA-256 (Secure Hash Algorithm 256-bit) produce un
    resumen único de 64 caracteres hexadecimales que es irreversible,
    lo que lo hace ideal para validar integridad de datos.
    
    Nota académica:
    - SHA-256 es una función hash unidireccional
    - Diferentes entradas siempre producen diferentes hashes
    - El mismo input siempre genera el mismo output
    - Es computacionalmente imposible revertir el proceso
    """
    
    @staticmethod
    def encriptar(texto: str) -> str:
        """
        Encripta un texto utilizando el algoritmo SHA-256.
        
        Convierte un texto plano en un hash único e irreversible de
        64 caracteres hexadecimales. Este método es determinístico:
        el mismo texto siempre produce el mismo hash.
        
        Args:
            texto (str): Texto plano a encriptar.
        
        Returns:
            str: Hash SHA-256 en formato hexadecimal (64 caracteres).
            
        Raises:
            Retorna cadena vacía si ocurre un error.
        
        Example:
            >>> encriptador = Encriptador()
            >>> hash_contrasena = encriptador.encriptar("contraseña123")
            >>> print(len(hash_contrasena))
            64
            >>> print(hash_contrasena)
            'e1d0814f0efb0105edfb4db3c36cbab3010323a7ca1d7c0c94bed6e7f9fcf0b7'
        
        Notas técnicas:
            - La función hashlib.sha256() recibe bytes, no strings
            - El método .encode('utf-8') convierte string a bytes
            - El método .hexdigest() retorna el hash como hexadecimal
        """
        try:
            # Paso 1: Validar que el input sea una cadena
            if not isinstance(texto, str):
                print("Error: El texto debe ser una cadena de caracteres.")
                return ""
            
            # Paso 2: Convertir el string a bytes usando encoding UTF-8
            # UTF-8 es el estándar para manejo de caracteres en Python
            texto_bytes = texto.encode('utf-8')
            
            # Paso 3: Crear un objeto hash SHA-256
            # hashlib.sha256() es la función de encriptación
            hash_object = hashlib.sha256(texto_bytes)
            
            # Paso 4: Retornar el hash en formato hexadecimal
            # hexdigest() convierte el hash a una cadena de 64 caracteres
            hash_hexadecimal = hash_object.hexdigest()
            
            return hash_hexadecimal
            
        except Exception as e:
            # Manejo de errores inesperados
            print(f"Error al encriptar: {str(e)}")
            return ""
    
    @staticmethod
    def verificar(texto_plano: str, texto_encriptado: str) -> bool:
        """
        Verifica si un texto plano coincide con un hash almacenado.
        
        Compara el hash de un texto plano con uno previamente almacenado.
        Este es el método estándar para validar contraseñas o datos
        sensibles sin guardarlos en texto plano.
        
        El proceso funciona así:
        1. Encriptar el texto plano proporcionado
        2. Comparar el resultado con el hash almacenado
        3. Si coinciden, el texto plano es válido
        
        Args:
            texto_plano (str): Texto plano a verificar.
            texto_encriptado (str): Hash SHA-256 almacenado (64 caracteres).
        
        Returns:
            bool: True si el texto plano coincide con el hash.
                  False si no coincide o hay error.
        
        Example:
            >>> encriptador = Encriptador()
            >>> contrasena_original = "micontraseña123"
            >>> hash_almacenado = encriptador.encriptar(contrasena_original)
            >>> 
            >>> # Verificar con contraseña correcta
            >>> resultado1 = encriptador.verificar(contrasena_original, hash_almacenado)
            >>> print(resultado1)
            True
            >>> 
            >>> # Verificar con contraseña incorrecta
            >>> resultado2 = encriptador.verificar("contraseña_incorrecta", hash_almacenado)
            >>> print(resultado2)
            False
        
        Casos de uso:
            - Validación de contraseñas al login
            - Verificación de integridad de datos
            - Auditoría de cambios en información sensible
        
        Notas de seguridad:
            - Nunca almacenar contraseñas en texto plano
            - Siempre comparar hashes en lugar de textos planos
            - Un hash válido del mismo texto siempre será idéntico
        """
        try:
            # Paso 1: Validar que ambos parámetros sean strings
            if not isinstance(texto_plano, str):
                print("Error: El texto plano debe ser una cadena.")
                return False
            
            if not isinstance(texto_encriptado, str):
                print("Error: El texto encriptado debe ser una cadena.")
                return False
            
            # Paso 2: Validar que el hash tiene la longitud correcta
            # SHA-256 siempre produce 64 caracteres hexadecimales
            if len(texto_encriptado) != 64:
                print(f"Error: Hash inválido. Se esperaban 64 caracteres, se recibieron {len(texto_encriptado)}.")
                return False
            
            # Paso 3: Encriptar el texto plano proporcionado
            hash_generado = Encriptador.encriptar(texto_plano)
            
            # Paso 4: Comparar el hash generado con el almacenado
            # La comparación es case-insensitive para mayor compatibilidad
            resultado = hash_generado.lower() == texto_encriptado.lower()
            
            return resultado
            
        except Exception as e:
            # Manejo de errores inesperados
            print(f"Error al verificar: {str(e)}")
            return False
