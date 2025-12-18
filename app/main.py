"""
Módulo principal de API_EVAL3 - Prueba integrada del sistema.

Este módulo ejecuta un flujo de prueba que integra todos los componentes:
API → Servicios → Base de Datos. Demuestra el funcionamiento completo
del sistema de Programación Orientada a Objetos.
"""

from app.api.jsonplaceholder_client import JsonPlaceholderClient
from app.config.conexion import Conexion
from app.services.usuario_service import UsuarioService
from app.services.post_service import PostService


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


# Punto de entrada del programa
if __name__ == "__main__":
    main()
