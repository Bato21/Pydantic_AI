import os
from dotenv import load_dotenv

print("--- Iniciando prueba de .env ---")

# 1. Intentamos cargar el archivo .env
#    Esta función buscará un archivo .env en la carpeta actual.
try:
    cargado_exitosamente = load_dotenv()
    
    if cargado_exitosamente:
        print("ÉXITO: Se encontró y cargó el archivo .env.")
    else:
        print("FALLO: No se pudo encontrar un archivo .env en este directorio.")

    # 2. Intentamos leer la variable del entorno
    api_key = os.environ.get("GOOGLE_API_KEY")

    if api_key:
        print("ÉXITO: La variable GOOGLE_API_KEY está en el entorno.")
        # Por seguridad, solo mostramos el inicio y el fin de la clave
        print(f"   Clave encontrada: {api_key[:4]}...{api_key[-4:]}")
    else:
        print("FALLO: La variable GOOGLE_API_KEY NO se encontró en el entorno.")

except ImportError:
    print("ERROR CRÍTICO: La biblioteca 'python-dotenv' no está instalada.")
    print("Por favor, ejecuta: pip install python-dotenv")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")

print("--- Prueba finalizada ---")