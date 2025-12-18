"""
Módulo de configuración centralizada para el proyecto.

Este archivo contiene las variables de configuración del proyecto,
incluyendo credenciales de base de datos y otros parámetros de entorno.

IMPORTANTE: Este archivo puede modificarse para ajustar la configuración
a tu entorno local. Cuando otro compañero clone el repositorio, debe
revisar y actualizar estos valores según su instalación local.
"""

import os

# =====================================================
# CONFIGURACIÓN DE BASE DE DATOS MYSQL
# =====================================================

# Host de la base de datos
# Por defecto: localhost (WAMP local)
# Puede sobrescribirse con variable de entorno: DB_HOST
DB_HOST = os.getenv('DB_HOST', 'localhost')

# Usuario de la base de datos
# Por defecto: root (usuario estándar de WAMP)
# Puede sobrescribirse con variable de entorno: DB_USER
DB_USER = os.getenv('DB_USER', 'root')

# Contraseña del usuario de base de datos
# Por defecto: vacío (WAMP no pide contraseña por defecto)
# Puede sobrescribirse con variable de entorno: DB_PASSWORD
DB_PASSWORD = os.getenv('DB_PASSWORD', '')

# Nombre de la base de datos
# Por defecto: api_eval3 (coincide con el DDL)
# Puede sobrescribirse con variable de entorno: DB_NAME
DB_NAME = os.getenv('DB_NAME', 'api_eval3')

# =====================================================
# NOTAS DE CONFIGURACIÓN
# =====================================================
# 
# Para cambiar la configuración sin modificar este archivo,
# puedes establecer variables de entorno:
#
# Windows PowerShell:
#   $env:DB_HOST = "tu_host"
#   $env:DB_USER = "tu_usuario"
#   $env:DB_PASSWORD = "tu_password"
#   $env:DB_NAME = "tu_base_datos"
#
# Windows CMD:
#   set DB_HOST=tu_host
#   set DB_USER=tu_usuario
#   set DB_PASSWORD=tu_password
#   set DB_NAME=tu_base_datos
#
# =====================================================
