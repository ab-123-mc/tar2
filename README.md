# Biblioteca Personal CLI

Este es un programa de línea de comandos desarrollado en Python para administrar una biblioteca personal. Permite registrar, listar, buscar, actualizar y eliminar información sobre tus libros. Los datos se almacenan en una base de datos SQLite local.

## Características

* **Agregar Libro**: Añade nuevos libros con título, autor, género y estado de lectura (leído/no leído).
* **Listar Libros**: Muestra todos los libros registrados en la biblioteca.
* **Buscar Libros**: Permite buscar libros por título o autor.
* **Actualizar Libro**: Modifica cualquier campo de un libro existente usando su ID.
* **Eliminar Libro**: Elimina un libro de la base de datos por su ID.

## Requisitos

* Python 3.x
* No se requieren librerías externas adicionales, ya que `sqlite3` viene incluido con Python.

## Cómo Ejecutar

1.  **Clonar el repositorio (si aplica) o descargar los arhojas:**
    Si no tienes un repositorio Git, simplemente asegúrate de tener los arhojas `app.py` y `database.py` en la misma carpeta.

2.  **Crear la Base de Datos:**
    Abre tu terminal (por ejemplo, PowerShell, CMD o bash) y navega hasta la carpeta donde guardaste los arhojas `app.py` y `database.py`.
    La base de datos `biblioteca.db` y la tabla `libros` se crearán automáticamente la primera vez que inicies `app.py`. También puedes ejecutar `python database.py` una vez para asegurarte.

3.  **Iniciar la Aplicación:**
    Desde la misma carpeta en tu terminal, ejecuta el siguiente comando:
    ```bash
    python app.py
    ```

4.  **Uso:**
    El programa mostrará un menú interactivo en la consola. Sigue las instrucciones y selecciona las opciones numéricas para realizar las operaciones deseadas.

## Estructura del Proyecto
