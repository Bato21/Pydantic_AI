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
    instructions="Eres un asistente experto en la Hackaton 2025."
    "Respondes preguntas usando tu herramienta 'consultar_documento'."
    "para encontrar información en el archivo 'hackaton.txt'."
    "Si no encuentras la info, dilo amablemente."
)

# --- Herramienta #1 (La herramienta RAG) ---
@agent.tool
def consultar_documento(ctx: RunContext, consulta: str) -> str:
    """
    Usa esta herramienta CUANDO el usuario pregunte sobre la Hackaton, 
    sus reglas, premios, el 'Proyecto Centinela', o el patrocinador 'TechCorp'.
    La 'consulta' debe ser la palabra o frase clave de la que el usuario quiere saber.
    """
    print(f"\n--- [Debug: Herramienta 'consultar_documento' llamada con consulta='{consulta}'] ---")
    
    try:
        resultados = []
        # Abrimos nuestro archivo de conocimiento
        with open("hackaton.txt", "r", encoding="utf-8") as f:
            for linea in f:
                # Búsqueda simple (sensible a minúsculas)
                if consulta.lower() in linea.lower():
                    resultados.append(linea.strip()) # strip() quita saltos de línea
        
        if not resultados:
            # Si la lista está vacía, no encontramos nada
            print("\n--- [Debug: No se encontró información.] ---")
            return f"No se encontró información específica sobre '{consulta}' en el documento."
        
        # Devolvemos todos los resultados encontrados, unidos
        print(f"\n--- [Debug: Se encontró la siguiente información: {resultados}] ---")
        return "\n".join(resultados)

    except FileNotFoundError:
        print("\n--- [Debug: ¡ERROR! No se encontró el archivo hackaton.txt] ---")
        # Este error es para el LLM, que lo traducirá
        return "Error crítico: El archivo de conocimiento 'hackaton.txt' no se encuentra."
    except Exception as e:
        print(f"\n--- [Debug: ¡ERROR! {e}] ---")
        return f"Error inesperado al leer el archivo: {e}"

# --- Herramienta #2 (Una herramienta que NO es RAG, para control) ---
@agent.tool
def sumar_numeros(ctx: RunContext, a: float, b: float) -> float:
    """Usa esta herramienta CUANDO el usuario necesite sumar dos números."""
    print(f"\n--- [Debug: Herramienta 'sumar_numeros' llamada con a={a}, b={b}] ---")
    return a + b

# --- Bucle de Chat (Igual que antes) ---
print("¡Chatbot con RAG iniciado!")
print("Puedes preguntar sobre 'hackaton.txt' o pedir sumas.")
print("Escribe 'salir' para terminar.")
print("-" * 30)

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
        
        # ATENCIÓN: Las llamadas RAG (con herramientas) también usan 2 llamadas
        # a la API. Descomenta esto si te da el error 429 (límite).
        # time.sleep(60)

    except KeyboardInterrupt:
        print("\nAgente: ¡Adiós!")
        break