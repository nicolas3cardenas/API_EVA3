-- Script DDL para crear la estructura de la base de datos
-- Compatible con WampServer y phpMyAdmin
-- Base de datos para proyecto de red social académica

-- =====================================================
-- Crear la base de datos si no existe
-- =====================================================
CREATE DATABASE IF NOT EXISTS api_eval3;

-- =====================================================
-- Usar la base de datos
-- =====================================================
USE api_eval3;

-- =====================================================
-- Tabla: usuario
-- Descripción: Almacena información de los usuarios del sistema
-- =====================================================
CREATE TABLE usuario (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(255) NOT NULL,
    correo VARCHAR(255) UNIQUE NOT NULL,
    creado_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Tabla: post
-- Descripción: Almacena las publicaciones (posts) de los usuarios
-- =====================================================
CREATE TABLE post (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    contenido TEXT NOT NULL,
    creado_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuario(id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- Índices adicionales para optimización de búsquedas
-- =====================================================
CREATE INDEX idx_post_usuario_id ON post(usuario_id);
CREATE INDEX idx_usuario_correo ON usuario(correo);
