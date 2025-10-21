from pydantic_ai import Agent
# 1. Esta importación es CORRECTA
from pydantic_ai.models.google import GoogleModel 

# --- ¡Sin clave de API aquí! ---

# 2. Creamos la instancia del modelo SIN el argumento 'api_key'
#    Esto forzará a Pydantic-AI a buscar la variable de entorno GOOGLE_API_KEY
gemini_model = GoogleModel(
    'gemini-pro-latest'
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