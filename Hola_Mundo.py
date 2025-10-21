from pydantic_ai import Agent

# 1. Instanciamos el Agente
#    - Le decimos qué modelo usar (en este caso, gemini-1.5-flash-latest).
#    - Pydantic-AI buscará automáticamente la variable de entorno GOOGLE_API_KEY.
#    - 'instructions' es el "System Prompt": define la personalidad o rol del agente.
agent = Agent(
    'gemini:gemini-1.5-flash-latest',
    instructions="Eres un historiador experto. Responde siempre de forma breve y precisa."
)

# 2. Definimos la pregunta
prompt = "¿De dónde viene la frase 'hola, mundo' en programación?"

print(f"Pregunta: {prompt}\n")

# 3. Ejecutamos el agente de forma síncrona
#    - .run_sync() espera a que el LLM complete toda la respuesta.
#    - 'result' es un objeto que contiene la respuesta y otra metadata.
result = agent.run_sync(prompt)

# 4. Imprimimos la respuesta
#    - La respuesta de texto plano se encuentra en el atributo 'output'.
print("Respuesta del Agente:")
print(result.output)