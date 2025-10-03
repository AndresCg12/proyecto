# 01_crear_db.py
import sqlite3

# --- DOCUMENTACIÓN ---
# Propósito: Este script inicializa la base de datos y crea las tablas necesarias.
# Tablas:
#   - estudiantes: Almacena el ID y el nombre de cada estudiante.
#   - asistencia: Guarda un registro cada vez que un estudiante escanea su QR.
# Uso: Ejecútalo una sola vez al inicio del proyecto.
# ---------------------

print("Conectando a la base de datos...")
# Se conectará a la base de datos 'asistencia.db' (la creará si no existe)
conn = sqlite3.connect('asistencia.db')
cursor = conn.cursor()
print("¡Conexión exitosa!")

# --- Creación de la tabla de estudiantes ---
print("Creando tabla 'estudiantes'...")
cursor.execute('''
CREATE TABLE IF NOT EXISTS estudiantes (
    id TEXT PRIMARY KEY,
    nombre TEXT NOT NULL
)
''')
print("Tabla 'estudiantes' creada.")

# --- Creación de la tabla de asistencia ---
print("Creando tabla 'asistencia'...")
cursor.execute('''
CREATE TABLE IF NOT EXISTS asistencia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    estudiante_id TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (estudiante_id) REFERENCES estudiantes (id)
)
''')
print("Tabla 'asistencia' creada.")

# --- Insertar algunos estudiantes de ejemplo ---
# Puedes cambiar o agregar los estudiantes que necesites.
# El 'id' debe ser único para cada uno.
estudiantes_ejemplo = [
    ('EST001', 'Ana García'),
    ('EST002', 'Carlos Pérez'),
    ('EST003', 'Sofía Rodríguez')
]

# Verificamos si ya existen para no insertarlos de nuevo
cursor.executemany('INSERT OR IGNORE INTO estudiantes (id, nombre) VALUES (?, ?)', estudiantes_ejemplo)
print(f"Se insertaron {cursor.rowcount} estudiantes de ejemplo.")

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos inicializada correctamente.")