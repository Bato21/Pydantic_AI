from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel
import time

# --- 1. IMPORTA LA BIBLIOTECA ---
from dotenv import load_dotenv

# --- 2. CARGA EL ARCHIVO .env ---
# Esto lee tu .env y carga la GOOGLE_API_KEY en el entorno
load_dotenv() 


# --- 1. Configuración del Modelo ---

gemini_model = GoogleModel(
    'gemini-2.5-flash',
    instructions=""
)

