// static/scanner.js

// --- DOCUMENTACIÓN ---
// Propósito: Controla la lógica de escaneo de QR en el navegador.
// Librería usada: html5-qrcode
// Flujo:
// 1. Espera a que el DOM esté completamente cargado.
// 2. Inicializa el escáner de QR en el elemento con id 'qr-reader'.
// 3. Cuando un QR es detectado con éxito (onScanSuccess), llama a la función.
// 4. La función onScanSuccess envía el ID del estudiante al servidor (backend).
// 5. Muestra el mensaje de respuesta del servidor en la página.
// ---------------------

document.addEventListener('DOMContentLoaded', (event) => {
    const resultsContainer = document.getElementById('qr-reader-results');
    let lastResult = null; // Para evitar envíos duplicados muy seguidos

    // Función que se ejecuta cuando se escanea un QR correctamente
    function onScanSuccess(decodedText, decodedResult) {
        // decodedText contiene el ID del estudiante (ej: "EST001")
        
        // Evita registrar el mismo código múltiples veces si se mantiene frente a la cámara
        if (decodedText !== lastResult) {
            lastResult = decodedText;
            resultsContainer.innerHTML = `Detectado: ${decodedText}. Registrando...`;
            resultsContainer.className = ''; // Limpiar clases CSS

            // Enviar el ID al servidor usando la API Fetch
            fetch('/registrar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id_estudiante: decodedText }),
            })
            .then(response => response.json()) // Convertir la respuesta a JSON
            .then(data => {
                // 'data' contiene la respuesta del servidor (ej: {status: 'success', message: '...'})
                console.log('Respuesta del servidor:', data);
                if (data.status === 'success') {
                    resultsContainer.innerHTML = `✅ ${data.message}`;
                    resultsContainer.className = 'success';
                } else {
                    resultsContainer.innerHTML = `❌ ${data.message}`;
                    resultsContainer.className = 'error';
                }
            })
            .catch(error => {
                console.error('Error al registrar:', error);
                resultsContainer.innerHTML = '❌ Error al conectar con el servidor.';
                resultsContainer.className = 'error';
            });
        }
    }

    // Crear una nueva instancia del escáner de QR
    let html5QrcodeScanner = new Html5QrcodeScanner(
      "qr-reader", // ID del contenedor donde se mostrará el video
      { fps: 10, qrbox: 250 } // Configuración: 10 frames por segundo, caja de escaneo de 250px
    );

    // Iniciar el escáner
    html5QrcodeScanner.render(onScanSuccess);
});