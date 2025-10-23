import time
from pydantic_ai import Agent, RunContext, ModelMessage
from pydantic_ai.models.google import GoogleModel 
import typing

# --- 1. IMPORTA LA BIBLIOTECA ---
from dotenv import load_dotenv

# --- 2. CARGA EL ARCHIVO .env ---
# Esto lee tu .env y carga la GOOGLE_API_KEY en el entorno
load_dotenv() 


# --- 1. Configuración del Modelo (Igual) ---
gemini_model = GoogleModel(
    'gemini-2.5-flash'
)

# --- 2. Creación del Agente (¡Con instrucciones mejoradas!) ---
agent = Agent(
    gemini_model,
    instructions=(
        "Eres un asistente de chat de calculadora. Respondes a las preguntas del usuario."
        "Tienes herramientas para sumar y multiplicar."
        "IMPORTANTE: Si el usuario te pide hacer una operación usando 'el resultado', "
        "'ese número', o 'eso', DEBES buscar en el historial de chat anterior para "
        "encontrar el número del resultado anterior y usarlo como argumento para tu herramienta."
    )
)

# --- 3. Herramienta #1 (Suma) ---
@agent.tool
def sumar_numeros(ctx: RunContext, a: int, b: int) -> int:
    """Usa esta herramienta CUANDO el usuario necesite sumar dos números enteros."""
    print(f"\n--- [Debug: Herramienta 'sumar_numeros' llamada con a={a}, b={b}] ---")
    return a + b

# --- 4. Herramienta #2 (Multiplicación) ---
@agent.tool
def multiplicar_numeros(ctx: RunContext, a: int, b: int) -> int:
    """Usa esta herramienta CUANDO el usuario quiera multiplicar dos números enteros."""
    print(f"\n--- [Debug: Herramienta 'multiplicar_numeros' llamada con a={a}, b={b}] ---")
    return a * b

# --- 5. Herramienta #5 (Resta) ---
@agent.tool
def restar_numeros(ctx: RunContext, a:int, b:int) -> int:
    """Usa esta herramienta CUANDO el usuario necesite restar dos números enteros."""
    print(f"\n--- [Debug: Herramienta 'restar_numeros' llamada con a={a}, b={b}] ---")
    return a-b

# --- 6. Bucle de Chat (La parte nueva) ---
print("¡Chatbot con memoria iniciado!")
print("Escribe 'salir' para terminar.")
print("-" * 30)

# 7. El historial es una LISTA de ModelMessage
messages: typing.List[ModelMessage] = []

# Mantenemos el agente vivo en este bucle
while True:
    try:
        # 1. Pedimos la entrada del usuario
        prompt = input("Usuario: ")
        
        # 2. Comando para salir del bucle
        if prompt.lower() == "salir":
            print("Agente: ¡Adiós!")
            break
        
        # 3. Ejecutamos el agente PASÁNDOLE el historial
        #    (Usando el parámetro 'message_history' de la doc)
        result = agent.run_sync(prompt, message_history=messages)
        
        # 4. ¡CRUCIAL! Actualizamos el historial con la nueva conversación
        #    'result.new_messages()' devuelve una lista de ModelMessage
        #    que podemos añadir a nuestra lista actual.
        messages.extend(result.new_messages())
        
        # 5. Imprimimos la respuesta del agente
        print(f"Agente: {result.output}")

        # NOTA: En el plan gratuito, podríamos necesitar una pausa
        # si el agente usa herramientas (2 llamadas a API).
        # Por ahora, lo dejamos así para probar la velocidad.
        # time.sleep(60) # Descomentar si tienes error 429

    except KeyboardInterrupt:
        # Permite salir con Ctrl+C
        print("\nAgente: ¡Adiós!")
        break