import sqlite3

DATABASE_NAME = "biblioteca.db"

def connect_db():
    """Conecta a la base de datos SQLite."""
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_table():
    """Crea la tabla 'libros' si no existe."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            genero TEXT,
            leido INTEGER NOT NULL DEFAULT 0 -- 0 para no leído, 1 para leído
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Base de datos '{DATABASE_NAME}' y tabla 'libros' verificadas/creadas correctamente.")
    
if __name__ == "__main__":
    # Este bloque se ejecutará solo si corres database.py directamente
    create_table()
