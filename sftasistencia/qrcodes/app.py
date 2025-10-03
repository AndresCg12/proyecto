# app.py
from flask import Flask, render_template, request, jsonify
import sqlite3
import datetime

# --- DOCUMENTACIÓN ---
# Propósito: Servidor web principal que maneja el escaneo y registro de asistencia.
# Rutas:
#   - '/': Muestra la página principal con la cámara para escanear.
#   - '/registrar': Endpoint que recibe el ID del estudiante, lo valida y lo guarda.
# Uso: Ejecútalo para iniciar el servidor y empezar a escanear.
# ---------------------

app = Flask(__name__)

# Función para conectar a la base de datos
def get_db_connection():
    conn = sqlite3.connect('asistencia.db')
    conn.row_factory = sqlite3.Row # Permite acceder a las columnas por nombre
    return conn

@app.route('/')
def index():
    """Ruta principal que renderiza la página de escaneo."""
    print("Cargando la página principal de escaneo...")
    return render_template('index.html')

@app.route('/registrar', methods=['POST'])
def registrar_asistencia():
    """Endpoint para registrar la asistencia de un estudiante."""
    # Obtiene el ID del estudiante del cuerpo de la solicitud (en formato JSON)
    id_estudiante = request.json.get('id_estudiante')
    
    if not id_estudiante:
        return jsonify({'status': 'error', 'message': 'No se recibió ID de estudiante.'}), 400

    print(f"Recibido ID: {id_estudiante}. Buscando en la base de datos...")
    
    conn = get_db_connection()
    # 1. Verificar si el estudiante existe
    estudiante = conn.execute('SELECT * FROM estudiantes WHERE id = ?', (id_estudiante,)).fetchone()
    
    if estudiante:
        # 2. Si existe, registrar la asistencia
        nombre_estudiante = estudiante['nombre']
        print(f"Estudiante encontrado: {nombre_estudiante}. Registrando asistencia...")
        conn.execute('INSERT INTO asistencia (estudiante_id) VALUES (?)', (id_estudiante,))
        conn.commit()
        conn.close()
        
        # Devolver una respuesta exitosa
        return jsonify({
            'status': 'success',
            'message': f'Asistencia registrada para {nombre_estudiante} a las {datetime.datetime.now().strftime("%H:%M:%S")}'
        })
    else:
        # 3. Si no existe, devolver un error
        conn.close()
        print(f"Error: Estudiante con ID {id_estudiante} no encontrado.")
        return jsonify({'status': 'error', 'message': 'Estudiante no encontrado.'}), 404

# Iniciar la aplicación
if __name__ == '__main__':
    # host='0.0.0.0' permite que otros dispositivos en tu red accedan a la aplicación
    app.run(debug=True, host='0.0.0.0', port=5000)