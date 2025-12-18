"""
Módulo principal de API_EVAL3 - Sistema interactivo.

Este módulo implementa un menú interactivo que permite:
1. Ejecutar prueba integrada automática
2. Importar datos desde API
3. Consultar datos de la BD
4. Eliminar registros

Demuestra la integración completa: API → Servicios → Base de Datos
en una arquitectura de Programación Orientada a Objetos.
"""

from app.api.jsonplaceholder_client import JsonPlaceholderClient
from app.config.conexion import Conexion
from app.services.usuario_service import UsuarioService
from app.services.post_service import PostService
from app.negocio.encriptador import Encriptador


def separador(titulo: str = "") -> None:
    """
    Imprime un separador visual en la consola.
    
    Args:
        titulo (str): Título opcional a mostrar en el separador.
    """
    if titulo:
        print(f"\n{'=' * 60}")
        print(f"  {titulo}")
        print(f"{'=' * 60}\n")
    else:
        print(f"\n{'-' * 60}\n")


def main() -> None:
    """
    Función principal que ejecuta el flujo integrado de pruebas.
    
    Secuencia:
    1. Inicializa conexión a MySQL
    2. Crea cliente de JSONPlaceholder
    3. Crea servicios con inyección de dependencias
    4. Importa usuarios desde API
    5. Importa posts desde API
    6. Lista usuarios de la BD
    7. Lista posts de la BD
    """
    try:
        # ============================================================
        # 1. INICIALIZACIÓN
        # ============================================================
        separador("INICIANDO SISTEMA API_EVAL3")
        
        print("1. Creando cliente de JSONPlaceholder...")
        cliente_api = JsonPlaceholderClient()
        print("   ✓ Cliente creado\n")
        
        print("2. Creando conexión a MySQL...")
        conexion_bd = Conexion()
        
        if not conexion_bd.conectar():
            print("   ✗ Error: No se pudo conectar a la base de datos.")
            print("   Verifique que MySQL está corriendo y la configuración es correcta.")
            return
        print("   ✓ Conexión exitosa\n")
        
        print("3. Creando servicios...")
        servicio_usuarios = UsuarioService(cliente_api, conexion_bd)
        servicio_posts = PostService(cliente_api, conexion_bd)
        print("   ✓ Servicios creados\n")
        
        # ============================================================
        # 2. IMPORTAR USUARIOS DESDE API
        # ============================================================
        separador("FASE 1: IMPORTAR USUARIOS DESDE JSONPLACEHOLDER")
        
        print("Ejecutando: UsuarioService.importar_desde_api()")
        print("Acción: Obtener usuarios de API → Convertir a objetos → Guardar en BD\n")
        
        resultado_usuarios = servicio_usuarios.importar_desde_api()
        
        if resultado_usuarios:
            print("\n✓ Usuarios importados exitosamente a la base de datos")
        else:
            print("\n✗ Error durante la importación de usuarios")
            conexion_bd.cerrar()
            return
        
        # ============================================================
        # 3. IMPORTAR POSTS DESDE API
        # ============================================================
        separador("FASE 2: IMPORTAR POSTS DESDE JSONPLACEHOLDER")
        
        print("Ejecutando: PostService.importar_desde_api()")
        print("Acción: Obtener posts de API → Convertir a objetos → Guardar en BD\n")
        
        resultado_posts = servicio_posts.importar_desde_api()
        
        if resultado_posts:
            print("\n✓ Posts importados exitosamente a la base de datos")
        else:
            print("\n✗ Error durante la importación de posts")
            conexion_bd.cerrar()
            return
        
        # ============================================================
        # 4. LISTAR USUARIOS DESDE BASE DE DATOS
        # ============================================================
        separador("FASE 3: LISTAR USUARIOS DESDE LA BASE DE DATOS")
        
        print("Ejecutando: UsuarioService.listar()")
        print("Acción: Consultar BD → Convertir filas a objetos → Mostrar datos\n")
        
        usuarios = servicio_usuarios.listar()
        
        if usuarios:
            print(f"✓ Se encontraron {len(usuarios)} usuario(s):\n")
            for usuario in usuarios[:5]:  # Mostrar los primeros 5
                print(f"  → ID: {usuario.id}")
                print(f"    Nombre: {usuario.nombre}")
                print(f"    Correo: {usuario.correo}")
                print()
            
            if len(usuarios) > 5:
                print(f"  ... y {len(usuarios) - 5} usuario(s) más\n")
        else:
            print("✗ No hay usuarios registrados en la base de datos\n")
        
        # ============================================================
        # 5. LISTAR POSTS DESDE BASE DE DATOS
        # ============================================================
        separador("FASE 4: LISTAR POSTS DESDE LA BASE DE DATOS")
        
        print("Ejecutando: PostService.listar()")
        print("Acción: Consultar BD → Convertir filas a objetos → Mostrar datos\n")
        
        posts = servicio_posts.listar()
        
        if posts:
            print(f"✓ Se encontraron {len(posts)} post(s):\n")
            for post in posts[:3]:  # Mostrar los primeros 3
                print(f"  → ID: {post.id}")
                print(f"    Usuario ID: {post.user_id}")
                print(f"    Título: {post.titulo}")
                print(f"    Contenido: {post.contenido[:80]}...")
                print()
            
            if len(posts) > 3:
                print(f"  ... y {len(posts) - 3} post(s) más\n")
        else:
            print("✗ No hay posts registrados en la base de datos\n")
        
        # ============================================================
        # 6. RESUMEN FINAL
        # ============================================================
        separador("PRUEBA INTEGRADA COMPLETADA")
        
        print("✓ SISTEMA FUNCIONANDO CORRECTAMENTE\n")
        print("Resumen de operaciones realizadas:")
        print(f"  • Usuarios importados y almacenados: {len(usuarios)}")
        print(f"  • Posts importados y almacenados: {len(posts)}")
        print(f"  • Base de datos: ACTIVA")
        print(f"  • Servicios: OPERACIONALES")
        
        print("\nEl sistema demuestra:")
        print("  ✓ Consumo de API REST (JSONPlaceholder)")
        print("  ✓ Programación Orientada a Objetos (Clases, Inyección de dependencias)")
        print("  ✓ Persistencia en Base de Datos MySQL")
        print("  ✓ Separación de responsabilidades (Capas)")
        
        # ============================================================
        # 7. CIERRE
        # ============================================================
        separador()
        
        # Cerrar la conexión
        conexion_bd.cerrar()
        
        print("\n✓ Aplicación finalizada correctamente\n")
        
    except KeyboardInterrupt:
        print("\n\n✗ Ejecución interrumpida por el usuario.")
        
    except Exception as e:
        print(f"\n✗ Error inesperado: {str(e)}")
        import traceback
        traceback.print_exc()


# ============================================================
# FUNCIONES DEL MENÚ INTERACTIVO
# ============================================================

def menu_principal() -> None:
    """
    Muestra el menú principal con opciones disponibles.
    
    Proporciona una interfaz clara para que el usuario seleccione
    qué operación desea realizar en el sistema.
    """
    print("\n" + "=" * 60)
    print("          MENÚ PRINCIPAL - API_EVAL3")
    print("=" * 60)
    print("1. Ejecutar prueba integrada (importar y listar)")
    print("2. Importar solo usuarios desde JSONPlaceholder")
    print("3. Importar solo posts desde JSONPlaceholder")
    print("4. Listar usuarios de la base de datos")
    print("5. Listar posts de la base de datos")
    print("6. Eliminar usuario por ID")
    print("7. Eliminar post por ID")
    print("8. Probar encriptación (capa de negocio)")
    print("0. Salir")
    print("=" * 60)


def opcion_1_prueba_integrada(servicio_usuarios: UsuarioService, servicio_posts: PostService) -> None:
    """
    OPCIÓN 1: Ejecuta el flujo de prueba integrada.
    
    Realiza el ciclo completo:
    - Importa usuarios desde API
    - Importa posts desde API
    - Lista usuarios de BD
    - Lista posts de BD
    
    Args:
        servicio_usuarios (UsuarioService): Servicio para usuarios.
        servicio_posts (PostService): Servicio para posts.
    """
    separador("PRUEBA INTEGRADA COMPLETA")
    
    # Importar usuarios
    print("\n[1/4] Importando usuarios...")
    resultado_usuarios = servicio_usuarios.importar_desde_api()
    
    # Importar posts
    print("\n[2/4] Importando posts...")
    resultado_posts = servicio_posts.importar_desde_api()
    
    if not resultado_usuarios or not resultado_posts:
        print("\n✗ Error en la importación")
        return
    
    # Listar usuarios
    print("\n[3/4] Listando usuarios...")
    usuarios = servicio_usuarios.listar()
    if usuarios:
        print(f"✓ Se encontraron {len(usuarios)} usuario(s)")
    
    # Listar posts
    print("\n[4/4] Listando posts...")
    posts = servicio_posts.listar()
    if posts:
        print(f"✓ Se encontraron {len(posts)} post(s)")
    
    print("\n✓ PRUEBA INTEGRADA COMPLETADA")


def opcion_2_importar_usuarios(servicio_usuarios: UsuarioService) -> None:
    """
    OPCIÓN 2: Importa solo usuarios desde JSONPlaceholder.
    
    Obtiene usuarios de la API y los almacena en la base de datos.
    
    Args:
        servicio_usuarios (UsuarioService): Servicio para usuarios.
    """
    separador("IMPORTAR USUARIOS")
    
    print("Conectando con JSONPlaceholder...")
    resultado = servicio_usuarios.importar_desde_api()
    
    if resultado:
        print("✓ Usuarios importados exitosamente")
    else:
        print("✗ Error durante la importación")


def opcion_3_importar_posts(servicio_posts: PostService) -> None:
    """
    OPCIÓN 3: Importa solo posts desde JSONPlaceholder.
    
    Obtiene posts de la API y los almacena en la base de datos.
    
    Args:
        servicio_posts (PostService): Servicio para posts.
    """
    separador("IMPORTAR POSTS")
    
    print("Conectando con JSONPlaceholder...")
    resultado = servicio_posts.importar_desde_api()
    
    if resultado:
        print("✓ Posts importados exitosamente")
    else:
        print("✗ Error durante la importación")


def opcion_4_listar_usuarios(servicio_usuarios: UsuarioService) -> None:
    """
    OPCIÓN 4: Lista todos los usuarios de la base de datos.
    
    Recupera y muestra todos los usuarios almacenados.
    
    Args:
        servicio_usuarios (UsuarioService): Servicio para usuarios.
    """
    separador("LISTAR USUARIOS")
    
    usuarios = servicio_usuarios.listar()
    
    if not usuarios:
        print("No hay usuarios registrados")
        return
    
    print(f"Se encontraron {len(usuarios)} usuario(s):\n")
    
    for usuario in usuarios:
        print(f"  ID: {usuario.id}")
        print(f"  Nombre: {usuario.nombre}")
        print(f"  Correo: {usuario.correo}")
        print()


def opcion_5_listar_posts(servicio_posts: PostService) -> None:
    """
    OPCIÓN 5: Lista todos los posts de la base de datos.
    
    Recupera y muestra todos los posts almacenados.
    
    Args:
        servicio_posts (PostService): Servicio para posts.
    """
    separador("LISTAR POSTS")
    
    posts = servicio_posts.listar()
    
    if not posts:
        print("No hay posts registrados")
        return
    
    print(f"Se encontraron {len(posts)} post(s):\n")
    
    for post in posts[:10]:  # Mostrar los primeros 10
        print(f"  ID: {post.id}")
        print(f"  Usuario ID: {post.user_id}")
        print(f"  Título: {post.titulo}")
        print(f"  Contenido: {post.contenido[:80]}...")
        print()
    
    if len(posts) > 10:
        print(f"  ... y {len(posts) - 10} post(s) más")


def opcion_6_eliminar_usuario(servicio_usuarios: UsuarioService) -> None:
    """
    OPCIÓN 6: Elimina un usuario por su ID.
    
    Solicita el ID del usuario y lo elimina de la BD.
    
    Args:
        servicio_usuarios (UsuarioService): Servicio para usuarios.
    """
    separador("ELIMINAR USUARIO")
    
    try:
        id_input = input("Ingrese el ID del usuario a eliminar: ").strip()
        
        # Validar que sea un número
        if not id_input.isdigit():
            print("✗ Error: El ID debe ser un número entero positivo")
            return
        
        usuario_id = int(id_input)
        
        # Eliminar el usuario
        resultado = servicio_usuarios.eliminar_por_id(usuario_id)
        
        if resultado:
            print(f"✓ Usuario {usuario_id} eliminado")
        else:
            print(f"✗ No se pudo eliminar el usuario {usuario_id}")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def opcion_7_eliminar_post(servicio_posts: PostService) -> None:
    """
    OPCIÓN 7: Elimina un post por su ID.
    
    Solicita el ID del post y lo elimina de la BD.
    
    Args:
        servicio_posts (PostService): Servicio para posts.
    """
    separador("ELIMINAR POST")
    
    try:
        id_input = input("Ingrese el ID del post a eliminar: ").strip()
        
        # Validar que sea un número
        if not id_input.isdigit():
            print("✗ Error: El ID debe ser un número entero positivo")
            return
        
        post_id = int(id_input)
        
        # Eliminar el post
        resultado = servicio_posts.eliminar_por_id(post_id)
        
        if resultado:
            print(f"✓ Post {post_id} eliminado")
        else:
            print(f"✗ No se pudo eliminar el post {post_id}")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def opcion_8_encriptacion() -> None:
    """
    OPCIÓN 8: Demuestra la capa de negocio con encriptación.
    
    Muestra cómo funciona la clase Encriptador de la capa de negocio
    usando el algoritmo SHA-256.
    """
    separador("DEMOSTRACIÓN - CAPA DE NEGOCIO: ENCRIPTACIÓN")
    
    # Crear instancia del encriptador
    encriptador = Encriptador()
    
    # Solicitar texto al usuario
    texto = input("Ingrese un texto a encriptar: ").strip()
    
    if not texto:
        print("✗ Debe ingresar un texto")
        return
    
    # Encriptar el texto
    print("\nProcesando encriptación SHA-256...")
    hash_resultado = encriptador.encriptar(texto)
    
    print(f"\nTexto original:     {texto}")
    print(f"Hash SHA-256:       {hash_resultado}")
    print(f"Longitud del hash:  {len(hash_resultado)} caracteres")
    
    # Verificación
    print("\n--- Verificación ---")
    texto_verificar = input("Ingrese el mismo texto para verificar: ").strip()
    
    resultado_verificacion = encriptador.verificar(texto_verificar, hash_resultado)
    
    if resultado_verificacion:
        print("✓ El texto coincide con el hash")
    else:
        print("✗ El texto NO coincide con el hash")


def bucle_menu(cliente_api: JsonPlaceholderClient, conexion_bd: Conexion) -> None:
    """
    Ejecuta el bucle principal del menú interactivo.
    
    Muestra el menú repetidamente hasta que el usuario seleccione salir.
    
    Args:
        cliente_api (JsonPlaceholderClient): Cliente para la API.
        conexion_bd (Conexion): Conexión a la base de datos.
    """
    # Crear servicios
    servicio_usuarios = UsuarioService(cliente_api, conexion_bd)
    servicio_posts = PostService(cliente_api, conexion_bd)
    
    # Bucle principal
    while True:
        try:
            # Mostrar menú
            menu_principal()
            
            # Obtener opción del usuario
            opcion = input("\nSeleccione una opción (0-8): ").strip()
            
            # Procesar opciones
            if opcion == "1":
                opcion_1_prueba_integrada(servicio_usuarios, servicio_posts)
                
            elif opcion == "2":
                opcion_2_importar_usuarios(servicio_usuarios)
                
            elif opcion == "3":
                opcion_3_importar_posts(servicio_posts)
                
            elif opcion == "4":
                opcion_4_listar_usuarios(servicio_usuarios)
                
            elif opcion == "5":
                opcion_5_listar_posts(servicio_posts)
                
            elif opcion == "6":
                opcion_6_eliminar_usuario(servicio_usuarios)
                
            elif opcion == "7":
                opcion_7_eliminar_post(servicio_posts)
                
            elif opcion == "8":
                opcion_8_encriptacion()
                
            elif opcion == "0":
                print("\n¡Gracias por usar API_EVAL3! Hasta luego.\n")
                break
                
            else:
                print("✗ Opción inválida. Intente nuevamente.")
            
            # Pausa para que el usuario vea el resultado
            input("\nPresione Enter para continuar...")
            
        except KeyboardInterrupt:
            print("\n\n✗ Programa interrumpido por el usuario")
            break
            
        except Exception as e:
            print(f"\n✗ Error: {str(e)}")


# Punto de entrada del programa
if __name__ == "__main__":
    main()
    
    # Después de ejecutar la prueba integrada, ofrecer el menú
    try:
        print("\n" + "=" * 60)
        print("¿Desea acceder al menú interactivo? (s/n): ", end="")
        respuesta = input().strip().lower()
        
        if respuesta == "s":
            # Reinicializar para el menú
            cliente_api = JsonPlaceholderClient()
            conexion_bd = Conexion()
            
            if conexion_bd.conectar():
                bucle_menu(cliente_api, conexion_bd)
                conexion_bd.cerrar()
            else:
                print("✗ No se pudo conectar a la base de datos")
    
    except Exception as e:
        print(f"Error: {str(e)}")
