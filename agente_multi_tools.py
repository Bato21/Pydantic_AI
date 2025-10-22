from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel 
import time

# --- 1. Configuración del Modelo (Igual) ---
gemini_model = GoogleModel(
    'gemini-pro-latest'
)

# --- 2. Creación del Agente (Igual) ---
agent = Agent(
    gemini_model,
    instructions="Eres un asistente experto. Ayudas con cálculos matemáticos o manipulación de texto."
)

# --- 3. Herramienta #1 (Matemáticas) ---
@agent.tool
def sumar_numeros(ctx: RunContext, a: int, b: int) -> int:
    """
    Usa esta herramienta CUANDO el usuario necesite sumar dos números enteros.
    """
    print(f"\n--- [Debug: Herramienta 'sumar_numeros' llamada con a={a}, b={b}] ---")
    return a + b

# --- 4. Herramienta #2 (Texto) ---
@agent.tool
def repetir_palabra(ctx: RunContext, palabra: str, veces: int) -> str:
    """
    Usa esta herramienta CUANDO el usuario quiera repetir una palabra un número específico de veces.
    """
    print(f"\n--- [Debug: Herramienta 'repetir_palabra' llamada con palabra='{palabra}', veces={veces}] ---")
    # Creamos la cadena repetida
    resultado = []
    for _ in range(veces):
        resultado.append(palabra)
    
    # Devolvemos un solo string, ej: "eco eco eco"
    return " ".join(resultado)

# --- 5. Los Prompts de Prueba ---
# Vamos a probar ambos casos en el mismo script

# Prueba 1: Debería llamar a sumar_numeros
prompt_1 = "Tengo 50 dólares y me dieron 75 más, ¿cuánto tengo?"

# Prueba 2: Debería llamar a repetir_palabra
prompt_2 = "Quiero que digas la palabra 'eco' 3 veces."

# --- 6. Ejecución de la Prueba 1 ---
print(f"Pregunta 1: {prompt_1}")
result_1 = agent.run_sync(prompt_1)
print("Respuesta 1:")
print(result_1.output)

print("\n" + "="*30)
print("Esperando 60 segundos para reiniciar el límite de la API gratuita...")
time.sleep(60) # <-- 2. Esperamos 60 segundos
print("Espera finalizada. Ejecutando Prueba 2.")
print("="*30 + "\n")

# --- 7. Ejecución de la Prueba 2 ---
print(f"Pregunta 2: {prompt_2}")
result_2 = agent.run_sync(prompt_2)
print("Respuesta 2:")
print(result_2.output)