import sqlite3 
from database import connect_db, create_table, DATABASE_NAME

# --- Funciones CRUD ---

def add_book(titulo, autor, genero, leido):
    """Agrega un nuevo libro a la base de datos."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO libros (titulo, autor, genero, leido) VALUES (?, ?, ?, ?)",
                       (titulo, autor, genero, leido))
        conn.commit()
        print(f"Libro '{titulo}' agregado correctamente.")
    except sqlite3.IntegrityError as e:
        print(f"Error al agregar libro: {e}")
    finally:
        conn.close()

def list_books():
    """Muestra todos los libros registrados en la base de datos."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, titulo, autor, genero, leido FROM libros")
        books = cursor.fetchall()

        if not books:
            print("\nNo hay libros registrados en la biblioteca.")
            return

        print("\n--- Libros en la Biblioteca ---")
        print(f"{'ID':<4} {'Título':<30} {'Autor':<25} {'Género':<20} {'Leído':<8}")
        print("-" * 90)

        for book in books:
            book_id, titulo, autor, genero, leido = book
            estado_leido = "Sí" if leido == 1 else "No"
            print(f"{book_id:<4} {titulo:<30} {autor:<25} {genero:<20} {estado_leido:<8}")
        print("-" * 90)

    except sqlite3.Error as e:
        print(f"Error al listar libros: {e}")
    finally:
        conn.close()

def search_books(query):
    """
    Busca libros en la base de datos por título o autor.
    La búsqueda no distingue entre mayúsculas y minúsculas y usa coincidencias parciales.
    """
    conn = connect_db()
    cursor = conn.cursor()
    try:
        sql_query = """
            SELECT id, titulo, autor, genero, leido
            FROM libros
            WHERE LOWER(titulo) LIKE ? OR LOWER(autor) LIKE ?
        """
        search_term = f"%{query.lower()}%"
        cursor.execute(sql_query, (search_term, search_term))
        books = cursor.fetchall()

        if not books:
            print(f"\nNo se encontraron libros que coincidan con '{query}'.")
            return

        print(f"\n--- Resultados de búsqueda para '{query}' ---")
        print(f"{'ID':<4} {'Título':<30} {'Autor':<25} {'Género':<20} {'Leído':<8}")
        print("-" * 90)

        for book in books:
            book_id, titulo, autor, genero, leido = book
            estado_leido = "Sí" if leido == 1 else "No"
            print(f"{book_id:<4} {titulo:<30} {autor:<25} {genero:<20} {estado_leido:<8}")
        print("-" * 90)

    except sqlite3.Error as e:
        print(f"Error al buscar libros: {e}")
    finally:
        conn.close()

def update_book(book_id, new_titulo=None, new_autor=None, new_genero=None, new_leido=None):
    """
    Actualiza la información de un libro existente por su ID.
    Solo actualiza los campos que se proporcionen (no None).
    """
    conn = connect_db()
    cursor = conn.cursor()
    try:
        updates = []
        params = []

        if new_titulo is not None:
            updates.append("titulo = ?")
            params.append(new_titulo)
        if new_autor is not None:
            updates.append("autor = ?")
            params.append(new_autor)
        if new_genero is not None:
            updates.append("genero = ?")
            params.append(new_genero)
        if new_leido is not None:
            updates.append("leido = ?")
            params.append(new_leido)

        if not updates:
            print("No se proporcionaron campos para actualizar.")
            return False

        sql_query = f"UPDATE libros SET {', '.join(updates)} WHERE id = ?"
        params.append(book_id)

        cursor.execute(sql_query, tuple(params))
        conn.commit()

        if cursor.rowcount == 0:
            print(f"No se encontró ningún libro con el ID {book_id}.")
            return False
        else:
            print(f"Libro con ID {book_id} actualizado correctamente.")
            return True

    except sqlite3.Error as e:
        print(f"Error al actualizar libro: {e}")
        return False
    finally:
        conn.close()

def delete_book(book_id):
    """Elimina un libro de la base de datos por su ID."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM libros WHERE id = ?", (book_id,))
        conn.commit()

        if cursor.rowcount == 0:
            print(f"No se encontró ningún libro con el ID {book_id} para eliminar.")
            return False
        else:
            print(f"Libro con ID {book_id} eliminado correctamente.")
            return True

    except sqlite3.Error as e:
        print(f"Error al eliminar libro: {e}")
        return False
    finally:
        conn.close()

# --- Menú Interactivo de la Aplicación ---
def main_menu():
    """Muestra el menú principal y maneja la interacción del usuario."""
    create_table() # Asegura que la tabla de libros exista al iniciar la app

    while True:
        print("\n--- Menú de Biblioteca Personal ---")
        print("1. Agregar nuevo libro")
        print("2. Listar todos los libros")
        print("3. Buscar libros por título o autor")
        print("4. Actualizar información de un libro")
        print("5. Eliminar libro")
        print("6. Salir")

        choice = input("Selecciona una opción: ").strip()

        if choice == '1':
            print("\n--- Agregar Nuevo Libro ---")
            titulo = input("Título: ").strip()
            autor = input("Autor: ").strip()
            genero = input("Género (opcional): ").strip()
            leido_input = input("¿Leído? (sí/no): ").strip().lower()
            leido = 1 if leido_input == 'sí' else 0

            if not titulo or not autor:
                print("Error: El título y el autor son obligatorios.")
            else:
                add_book(titulo, autor, genero if genero else None, leido)

        elif choice == '2':
            list_books()

        elif choice == '3':
            print("\n--- Buscar Libros ---")
            query = input("Buscar por título o autor: ").strip()
            if not query:
                print("La consulta de búsqueda no puede estar vacía.")
            else:
                search_books(query)

        elif choice == '4':
            print("\n--- Actualizar Libro ---")
            try:
                book_id = int(input("Introduce el ID del libro a actualizar: ").strip())
                print("Deja en blanco los campos que no quieras actualizar.")
                new_titulo = input("Nuevo título (dejar en blanco para no cambiar): ").strip()
                new_autor = input("Nuevo autor (dejar en blanco para no cambiar): ").strip()
                new_genero = input("Nuevo género (dejar en blanco para no cambiar): ").strip()
                new_leido_input = input("¿Nuevo estado (leído: sí/no, dejar en blanco para no cambiar)?: ").strip().lower()

                new_titulo = new_titulo if new_titulo else None
                new_autor = new_autor if new_autor else None
                new_genero = new_genero if new_genero else None
                new_leido = None
                if new_leido_input == 'sí':
                    new_leido = 1
                elif new_leido_input == 'no':
                    new_leido = 0

                update_book(book_id, new_titulo, new_autor, new_genero, new_leido)
            except ValueError:
                print("Error: El ID del libro debe ser un número entero.")

        elif choice == '5':
            print("\n--- Eliminar Libro ---")
            try:
                book_id = int(input("Introduce el ID del libro a eliminar: ").strip())
                delete_book(book_id)
            except ValueError:
                print("Error: El ID del libro debe ser un número entero.")

        elif choice == '6':
            print("Saliendo de la aplicación. ¡Hasta pronto!")
            break

        else:
            print("Opción no válida. Por favor, intenta de nuevo.")

if __name__ == "__main__":
    main_menu()
