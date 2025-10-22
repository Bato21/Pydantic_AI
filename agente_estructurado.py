from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel
from pydantic import BaseModel, Field # <-- 1. Importamos Pydantic

# --- 2. Definimos nuestro modelo de SALIDA ---
# Esta es la estructura que *forzaremos* a que el LLM devuelva.
class RespuestaCalculo(BaseModel):
    resultado: int = Field(description="El resultado numérico de la operación.")
    comentario: str = Field(description="Un breve comentario sobre la operación realizada.")

# --- 3. Configuración del Modelo (Igual) ---
gemini_model = GoogleModel(
    'gemini-pro-latest'
)

# --- 4. Creación del Agente (¡Con un cambio!) ---
agent = Agent(
    gemini_model,
    instructions="Eres un asistente de calculadora. Usas tus herramientas.",
    # ¡Aquí le decimos al agente que TODA respuesta debe ser un objeto RespuestaCalculo!
    output_type=RespuestaCalculo 
)

# --- 5. Definición de la Herramienta (Igual) ---
@agent.tool
def sumar_numeros(ctx: RunContext, a: int, b: int) -> int:
    """Usa esta herramienta para sumar dos números enteros."""
    print(f"\n--- [Debug: Herramienta 'sumar_numeros' llamada con a={a}, b={b}] ---")
    return a + b

# --- 6. El Prompt (Igual) ---
prompt = "Por favor, ¿me puedes ayudar a calcular 123 + 456?"

print(f"Pregunta: {prompt}\n")

# --- 7. Ejecución ---
result = agent.run_sync(prompt)

# --- 8. Resultado ---
print("\nRespuesta del Agente (como objeto Python):")
# 'result.output' ya no es un string, ¡es una instancia de RespuestaCalculo!
print(result.output)

print("\nAccediendo a los campos (como en Pydantic):")
print(f"Comentario: {result.output.comentario}")
print(f"Resultado: {result.output.resultado}")