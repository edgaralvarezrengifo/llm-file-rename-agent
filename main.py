from agents.analyzer_agent import AnalyzerAgent
from agents.rename_agent import RenameAgent
import os, time

# Configuración del modelo Ollama
LLM_CONFIG = {
    "config_list": [
        {
            "model": "phi3:mini",
            "base_url": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434") + "/v1",
            "api_key": "ollama",  # Ollama no requiere API key, pero AutoGen espera una
        }
    ],
    "cache_seed": None,  # Desactivar cache
}

# Inicialización de agentes
print("🔧 Inicializando agentes...")
analyzer = AnalyzerAgent(
    name="Analyzer",
    system_message="Eres un agente que analiza documentos y describe su contenido de forma clara y concisa en máximo 2 frases.",
    llm_config=LLM_CONFIG
)

renamer = RenameAgent(
    name="Renamer",
    system_message="Eres un agente que genera nombres de archivo descriptivos en formato snake_case, sin acentos ni caracteres especiales. Responde SOLO con el nombre del archivo, nada más.",
    llm_config=LLM_CONFIG
)

input_dir = "data/input"
print("🤖 Agente de renombramiento iniciado. Esperando archivos...\n")

while True:
    files_processed = False
    
    for file in os.listdir(input_dir):
        if not file.lower().endswith((".pdf", ".txt")):
            continue

        file_path = os.path.join(input_dir, file)
        files_processed = True
        
        print(f"{'='*60}")
        print(f"📄 Procesando archivo: {file}")
        print(f"{'='*60}")

        # Paso 1: Extraer contenido del archivo
        print("\n🔍 Paso 1: Leyendo contenido del archivo...")
        description = analyzer.analyze_file(file_path)
        print(f"✓ Análisis completado")
        print(f"📝 Descripción: {description}\n")

        # Paso 2: Generar nombre basado en la descripción
        print("✏️  Paso 2: Generando nuevo nombre...")
        new_name = renamer.rename_based_on_description(file_path, description)
        print(f"✅ Archivo renombrado como: {os.path.basename(new_name)}")
        print(f"{'='*60}\n")
    
    if not files_processed:
        print("💤 No hay archivos para procesar. Esperando...")
    
    time.sleep(10)
