from pydantic_ai import Agent, RunContext 
from pydantic_ai.models.google import GoogleModel 

# --- Configuración del Modelo ---
gemini_model = GoogleModel(
    'gemini-pro-latest'
)

# --- Creación del Agente ---
agent = Agent(
    gemini_model,
    instructions="Eres un asistente de calculadora. Usas tus herramientas para responder."
)

# --- Definición de la Herramienta (Con la corrección) ---

@agent.tool
def sumar_numeros(ctx: RunContext, a: int, b: int) -> int: 
    """
    Usa esta herramienta para sumar dos números enteros.
    El 'docstring' (esto que estás leyendo) es MUY importante,
    el LLM lo usa para entender qué hace la herramienta.
    """
    # Aunque 'ctx' no se usa aquí, debe estar en la firma de la función.
    print(f"\n--- [Debug: Herramienta 'sumar_numeros' llamada con a={a}, b={b}] ---")
    return a + b

# --- El Prompt ---
prompt = "Por favor, ¿me puedes ayudar a calcular 123 + 456?"

print(f"Pregunta: {prompt}\n")

# --- Ejecución ---
result = agent.run_sync(prompt)

# --- Resultado ---
print("\nRespuesta del Agente:")
print(result.output)