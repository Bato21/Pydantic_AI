import google.generativeai as genai
import os
import sys

print("Iniciando script de verificación de modelos...")

# 1. Lee la clave desde la variable de entorno
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    print("\n--- ERROR ---")
    print("No se pudo encontrar la variable de entorno GOOGLE_API_KEY.")
    print("Asegúrate de ejecutar 'set GOOGLE_API_KEY=...' en esta terminal primero.")
    sys.exit() # Termina el script si no hay clave

print("Clave de API encontrada. Configurando cliente de Google...")

try:
    genai.configure(api_key=api_key)
    
    print("Buscando modelos disponibles...")
    
    # 2. Llama a la API para listar los modelos
    
    print("\n--- Modelos Disponibles (que soportan 'generateContent') ---")
    count = 0
    # Iteramos sobre todos los modelos que Google nos devuelve
    for m in genai.list_models():
        # Filtramos solo por los modelos que pueden "generar contenido"
        # (que es lo que 'pydantic-ai' necesita)
        if 'generateContent' in m.supported_generation_methods:
            print(f"Modelo encontrado: {m.name}")
            count += 1
    
    if count == 0:
        print("\n¡Alerta! No se encontraron modelos que soporten 'generateContent' con esta clave.")
    else:
        print(f"\nTotal de modelos encontrados: {count}")

except Exception as e:
    print(f"\n--- ERROR AL CONECTAR CON GOOGLE ---")
    print(f"Ocurrió un error: {e}")
    print("Esto podría ser un problema con la clave de API o la configuración del proyecto.")

print("\nScript finalizado.")