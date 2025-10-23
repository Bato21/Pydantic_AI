from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel
from pydantic import BaseModel, Field

# --- 1. IMPORTA LA BIBLIOTECA ---
from dotenv import load_dotenv

# --- 2. CARGA EL ARCHIVO .env ---
# Esto lee tu .env y carga la GOOGLE_API_KEY en el entorno
load_dotenv() 

# --- 3. Definimos nuestro modelo de SALIDA ---
class RespuestaCalculo(BaseModel):
    resultado: int = Field(description="El resultado numérico de la operación.")
    comentario: str = Field(description="Un breve comentario sobre la operación realizada.")

# --- 4. Configuración del Modelo (Igual) ---
# Ahora GoogleModel() SÍ encontrará la clave que 'load_dotenv()' cargó
gemini_model = GoogleModel(
    'gemini-2.5-flash'
)

# --- 5. Creación del Agente (¡Con un cambio!) ---
agent = Agent(
    gemini_model,
    instructions="Eres un asistente de calculadora. Usas tus herramientas.",
    output_type=RespuestaCalculo 
)

# --- 6. Definición de la Herramienta (Igual) ---
@agent.tool
def sumar_numeros(ctx: RunContext, a: int, b: int) -> int:
    """Usa esta herramienta para sumar dos números enteros."""
    print(f"\n--- [Debug: Herramienta 'sumar_numeros' llamada con a={a}, b={b}] ---")
    return a + b

# --- 7. El Prompt (Igual) ---
prompt = "Por favor, ¿me puedes ayudar a calcular 123 + 456?"

print(f"Pregunta: {prompt}\n")

# --- 8. Ejecución ---
result = agent.run_sync(prompt)

# --- 9. Resultado ---
print("\nRespuesta del Agente (como objeto Python):")
print(result.output)

print("\nAccediendo a los campos (como en Pydantic):")
print(f"Comentario: {result.output.comentario}")
print(f"Resultado: {result.output.resultado}")