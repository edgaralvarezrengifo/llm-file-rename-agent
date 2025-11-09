from autogen import AssistantAgent
import os, re, csv
from datetime import datetime

class RenameAgent(AssistantAgent):
    """
    Agente encargado de generar un nuevo nombre de archivo basado en la descripción
    proporcionada por el agente analizador. Realiza el renombramiento físico del archivo
    en el sistema local, evitando duplicados y registrando la operación.
    """

    def __init__(self, name, llm_config):
        super().__init__(name=name, llm_config=llm_config)
        self.output_dir = "data/output"
        self.log_file = os.path.join(self.output_dir, "rename_log.csv")
        os.makedirs(self.output_dir, exist_ok=True)

        # Crear encabezado del log si no existe
        if not os.path.exists(self.log_file):
            with open(self.log_file, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "original_name", "new_name", "status"])

    def rename_based_on_description(self, original_path, description):
        """Genera un nuevo nombre de archivo a partir de la descripción semántica."""

        # Generar un nombre basado en la descripción
        prompt = (
            "Genera un nombre de archivo corto, claro y en formato snake_case, "
            "sin caracteres especiales ni acentos, basado en esta descripción:\n"
            f"{description}"
        )
        proposed_name = self.llm.generate(prompt)
        clean_name = re.sub(r'[^a-zA-Z0-9_]', '', proposed_name.strip().lower().replace(" ", "_"))

        # Obtener extensión original
        extension = os.path.splitext(original_path)[1]
        base_name = f"{clean_name}{extension}"
        new_path = os.path.join(self.output_dir, base_name)

        #  Manejar duplicados (añade _v2, _v3, etc.)
        if os.path.exists(new_path):
            base, ext = os.path.splitext(new_path)
            i = 2
            while os.path.exists(f"{base}_v{i}{ext}"):
                i += 1
            new_path = f"{base}_v{i}{ext}"

        # Mover archivo al directorio de salida
        try:
            os.rename(original_path, new_path)
            status = "renombrado_exitosamente"
            print(f"✅ Archivo renombrado como: {os.path.basename(new_path)}")

        except Exception as e:
            status = f"error: {str(e)}"
            print(f"❌ Error al mover el archivo {original_path}: {e}")

        # Registrar la operación en el log CSV
        with open(self.log_file, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                os.path.basename(original_path),
                os.path.basename(new_path),
                status
            ])

        return new_path
