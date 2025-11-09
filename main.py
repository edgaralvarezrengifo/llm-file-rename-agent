from agents.analyzer_agent import AnalyzerAgent
from agents.rename_agent import RenameAgent
import os, time

LLM_CONFIG = {
    "model": "mistral",
    "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
}

analyzer = AnalyzerAgent(name="Analyzer", llm_config=LLM_CONFIG)
renamer = RenameAgent(name="Renamer", llm_config=LLM_CONFIG)

input_dir = "data/input"
output_dir = "data/output"

print("🧠 Agente de renombramiento iniciado. Esperando archivos...")

while True:
    for file in os.listdir(input_dir):
        if not file.lower().endswith((".txt", ".pdf")):
            continue

        src = os.path.join(input_dir, file)
        print(f"📄 Procesando: {file}")
        description = analyzer.analyze_file(src)
        new_name = renamer.rename_based_on_description(src, description)
        print(f"✅ Nuevo nombre: {os.path.basename(new_name)}")

    time.sleep(10)