from autogen import GroupChat, UserProxyAgent
from agents.analyzer_agent import AnalyzerAgent
from agents.rename_agent import RenameAgent
import os, time

# Configuración del modelo Ollama
LLM_CONFIG = {
    "model": "mistral",
    "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
}

# Inicialización de agentes
analyzer = AnalyzerAgent(name="Analyzer", llm_config=LLM_CONFIG)
renamer = RenameAgent(name="Renamer", llm_config=LLM_CONFIG)

# Crear un GroupChat donde ambos agentes colaboran
group = GroupChat(
    agents=[analyzer, renamer],
    messages=[]
)

# Agente usuario (proxy del sistema)
user = UserProxyAgent(name="SystemProxy", group_chat=group)

input_dir = "data/input"
print("🤖 Agente de renombramiento iniciado. Esperando archivos...")

while True:
    for file in os.listdir(input_dir):
        if not file.lower().endswith((".pdf", ".txt")):
            continue

        file_path = os.path.join(input_dir, file)
        print(f"\n📄 Procesando archivo: {file}")

        # Agente 1: análisis del contenido
        description = analyzer.analyze_file(file_path)

        # Conversación multiagente (coordinada)
        message = f"El archivo contiene el siguiente contenido:\n{description}\nGenera un nombre de archivo adecuado."
        result = user.initiate_chat(message)

        # Agente 2: ejecutar el renombramiento localmente
        new_name = renamer.rename_based_on_description(file_path, str(result))
        print(f"✅ Archivo renombrado como: {os.path.basename(new_name)}")

    time.sleep(10)
