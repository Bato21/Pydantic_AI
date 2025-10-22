import time
from pydantic_ai import Agent, RunContext, ModelMessage
from pydantic_ai.models.google import GoogleModel 
import typing

# --- Configuración del Modelo ---
gemini_model = GoogleModel(
    'gemini-pro-latest'
)

# --- Creación del Agente ---
agent = Agent(
    gemini_model,
    instructions="Eres un asistente matemático. Ayudas con cálculos y explicas los errores si ocurren."
)

# --- Herramienta #1 (Suma) ---
@agent.tool
def sumar_numeros(ctx: RunContext, a: float, b: float) -> float:
    """Usa esta herramienta CUANDO el usuario necesite sumar dos números."""
    print(f"\n--- [Debug: Herramienta 'sumar_numeros' llamada con a={a}, b={b}] ---")
    return a + b

# --- Herramienta #2 (División - ¡Puede fallar!) ---
@agent.tool
def dividir_numeros(ctx: RunContext, a: float, b: float) -> float:
    """Usa esta herramienta CUANDO el usuario quiera dividir un número (a) por otro (b)."""
    print(f"\n--- [Debug: Herramienta 'dividir_numeros' llamada con a={a}, b={b}] ---")
    
    if b == 0:
        # 1. ¡Aquí lanzamos una excepción!
        # Este 'raise' será capturado por pydantic-ai, no por Python.
        print("\n--- [Debug: ¡ERROR! Se detectó división por cero.] ---")
        raise ValueError("No se puede dividir por cero. Es un error matemático fundamental.")
    
    return a / b

# --- Bucle de Chat (Igual que antes) ---
print("¡Chatbot con manejo de errores iniciado!")
print("Escribe 'salir' para terminar.")
print("-" * 30)

# El historial es una LISTA de ModelMessage
messages: typing.List[ModelMessage] = [] 

while True:
    try:
        prompt = input("Usuario: ")
        
        if prompt.lower() == "salir":
            print("Agente: ¡Adiós!")
            break
        
        result = agent.run_sync(prompt, message_history=messages)
        
        messages.extend(result.new_messages())
        
        print(f"Agente: {result.output}")
        
        # NOTA: Si te da error 429 (límite de velocidad), descomenta la línea de abajo
        # time.sleep(60)

    except KeyboardInterrupt:
        print("\nAgente: ¡Adiós!")
        break