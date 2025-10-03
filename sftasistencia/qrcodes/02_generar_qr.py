# 02_generar_qr.py
import sqlite3
import qrcode
import os

# --- DOCUMENTACIÓN ---
# Propósito: Lee los estudiantes de la base de datos y genera un código QR para cada uno.
# El QR contendrá el ID único del estudiante (ej. "EST001").
# Uso: Ejecútalo después de crear la base de datos para generar los QR.
# ---------------------

# Directorio donde se guardarán los códigos QR
output_dir = 'qrcodes'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Directorio '{output_dir}' creado.")

print("Conectando a la base de datos...")
conn = sqlite3.connect('asistencia.db')
cursor = conn.cursor()
print("¡Conexión exitosa!")

# Seleccionar todos los estudiantes
cursor.execute('SELECT id, nombre FROM estudiantes')
estudiantes = cursor.fetchall()
conn.close()

if not estudiantes:
    print("No se encontraron estudiantes en la base de datos.")
else:
    print(f"Generando QR para {len(estudiantes)} estudiantes...")
    # Iterar sobre cada estudiante y crear su QR
    for id_estudiante, nombre in estudiantes:
        # La información que guardaremos en el QR es el ID del estudiante
        qr_data = id_estudiante
        
        # Crear el objeto QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Crear la imagen del QR
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Guardar la imagen en la carpeta 'qrcodes'
        # El nombre del archivo será el ID del estudiante (ej. EST001.png)
        file_path = os.path.join(output_dir, f'{id_estudiante}.png')
        img.save(file_path)
        print(f"  - QR para {nombre} ({id_estudiante}) guardado en {file_path}")

print("Proceso de generación de QR finalizado.")