import subprocess
import webbrowser
import time
import requests
import os

# Verificar si el archivo app.py existe en el directorio actual
current_directory = os.path.dirname(os.path.abspath(__file__))
app_path = os.path.join(current_directory, "app.py")

if not os.path.exists(app_path):
    print(f"Error: No se encuentra el archivo app.py en {current_directory}")
    exit(1)

# Función para verificar si el servidor de Streamlit está en funcionamiento
def check_server():
    try:
        response = requests.get("http://localhost:8501")
        if response.status_code == 200:
            return True
    except requests.ConnectionError:
        return False

# Ejecutar el comando de Streamlit para iniciar la aplicación
process = subprocess.Popen(["streamlit", "run", app_path])

# Esperar y verificar que el servidor de Streamlit esté en funcionamiento
server_started = False
for _ in range(30):  # Intentar durante 30 segundos
    if check_server():
        server_started = True
        break
    time.sleep(1)

if server_started:
    # Abrir el navegador web
    webbrowser.open("http://localhost:8501")
else:
    print("El servidor de Streamlit no se inició correctamente.")

# Mantener el script en ejecución mientras el proceso de Streamlit está activo
try:
    process.wait()
except KeyboardInterrupt:
    process.terminate()
