from autogen import AssistantAgent
import os, re, csv
from datetime import datetime

class RenameAgent(AssistantAgent):
    """
    Agente encargado de generar un nuevo nombre de archivo basado en la descripción
    proporcionada por el agente analizador. Realiza el renombramiento físico del archivo
    en el sistema local, evitando duplicados y registrando la operación.
    """

    def __init__(self, name, llm_config, system_message=None):
        super().__init__(name=name, llm_config=llm_config, system_message=system_message)
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
            "Analiza el documento y crea un nombre de archivo descriptivo.\n\n"
            "PASO 1: Identifica el TIPO EXACTO de documento:\n"
            "   - Si dice 'certificado': usa 'certificado'\n"
            "   - Si dice 'tesis': usa 'tesis'\n"
            "   - Si dice 'solicitud': usa 'solicitud'\n"
            "   - Si dice 'informe': usa 'informe'\n"
            "   - Si dice 'contrato': usa 'contrato'\n\n"
            "PASO 2: Identifica el tema o propósito específico (2-3 palabras)\n"
            "PASO 3: Si hay un nombre de persona, inclúyelo al final (apellido)\n\n"
            "REGLAS ESTRICTAS:\n"
            "1. MÁXIMO 5 palabras en español\n"
            "2. Formato: tipo_tema_concepto_apellido\n"
            "3. Sin acentos (á→a, é→e, í→i, ó→o, ú→u, ñ→n)\n"
            "4. TODO en minúsculas\n"
            "5. NO agregues números ni fechas\n"
            "6. NO uses palabras en inglés\n\n"
            "Ejemplos correctos:\n"
            "- certificado_materias_cursadas_alvarez\n"
            "- certificado_maestria_sistemas_alvarez\n"
            "- tesis_ingenieria_software_alvarez\n"
            "- solicitud_extension_plazo_garcia\n"
            "- contrato_prestacion_servicios_lopez\n\n"
            f"Descripción del documento:\n{description[:300]}\n\n"
            "Responde SOLO con el nombre (máximo 5 palabras):"
        )

        print(f"   Generando nombre para: {description[:80]}...")

        # Usar el método generate_oai_reply de AutoGen
        messages = [{"role": "user", "content": prompt}]
        response = self.generate_oai_reply(messages)

        # extract text from response tuple
        if isinstance(response, tuple):
            proposed_name = response[1] if len(response) > 1 else response[0]
        else:
            proposed_name = response

        # Limpiar el nombre (eliminar comillas, puntos, etc)
        proposed_name = str(proposed_name).strip().replace('"', '').replace("'", "").split('\n')[0]
        clean_name = re.sub(r'[^a-zA-Z0-9_]', '', proposed_name.lower().replace(" ", "_"))

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
            print(f":white_check_mark: Archivo renombrado como: {os.path.basename(new_path)}")

        except Exception as e:
            status = f"error: {str(e)}"
            print(f":x: Error al mover el archivo {original_path}: {e}")

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
