from pydantic_ai import Agent
# 1. Esta importación es CORRECTA
from pydantic_ai.models.google import GoogleModel 

# --- 1. IMPORTA LA BIBLIOTECA ---
from dotenv import load_dotenv

# --- 2. CARGA EL ARCHIVO .env ---
# Esto lee tu .env y carga la GOOGLE_API_KEY en el entorno
load_dotenv() 


# 2. Creamos la instancia del modelo SIN el argumento 'api_key'
#    Esto forzará a Pydantic-AI a buscar la variable de entorno GOOGLE_API_KEY
gemini_model = GoogleModel(
    'gemini-2.5-flash'
)

# 3. Instanciamos el Agente (esto no cambia)
agent = Agent(
    gemini_model,
    instructions="Eres un historiador experto. Responde siempre de forma breve y precisa."
)

# 4. Definimos la pregunta
prompt = "¿De dónde viene la frase 'hola, mundo' en programación?"

print(f"Pregunta: {prompt}\n")

# 5. Ejecutamos el agente
result = agent.run_sync(prompt)

# 6. Imprimimos la respuesta
print("Respuesta del Agente:")
print(result.output)