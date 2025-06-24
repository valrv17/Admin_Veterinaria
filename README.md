# Sistema de Gestión de Veterinaria

Este proyecto implementa un sistema básico de gestión para una clínica veterinaria utilizando `SQLite` como base de datos. Permite administrar información sobre dueños de mascotas, las mascotas mismas y las consultas veterinarias asociadas a ellas.

## Características

* **Gestión de Dueños**:
    * Registrar nuevos dueños con nombre, teléfono y dirección.
    * Consultar todos los dueños registrados.
    * Actualizar información de dueños existentes.
    * Eliminar registros de dueños.
* **Gestión de Mascotas**:
    * Registrar nuevas mascotas con nombre, especie, raza, edad y su dueño asociado.
    * Consultar todas las mascotas.
    * Consultar mascotas por el ID del dueño.
    * Actualizar información de mascotas existentes.
    * Eliminar registros de mascotas (elimina en cascada las consultas asociadas).
* **Gestión de Consultas**:
    * Registrar nuevas consultas con fecha, motivo, diagnóstico y la mascota asociada.
    * Consultar todas las consultas.
    * Consultar consultas por el ID de la mascota.
    * Actualizar información de consultas existentes.
    * Eliminar registros de consultas.
* **Base de Datos SQLite**: Utiliza una base de datos `SQLite` ligera y fácil de integrar.
* **Menú Interactivo**: Ofrece una interfaz de consola interactiva para facilitar la gestión.

## Requisitos

* Python 3.x

## Instalación

1.  Clona este repositorio o descarga el archivo `admin_veterinaria.py`.
2.  No se requieren instalaciones de librerías adicionales, ya que `sqlite3` y `os` son módulos estándar de Python.

## Uso

Para ejecutar el programa, simplemente abre una terminal o línea de comandos, navega hasta el directorio donde guardaste el archivo y ejecuta:

```
python admin_veterinaria.py
