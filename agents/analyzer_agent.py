from autogen import AssistantAgent
import PyPDF2, os

class AnalyzerAgent(AssistantAgent):
    def analyze_file(self, file_path):
        content = ""
        if file_path.endswith(".pdf"):
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages[:3]:  # Solo primeras 3 páginas para ser más rápido
                    content += page.extract_text()
        elif file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = "Tipo de archivo no soportado."

        # Limitar contenido para acelerar análisis
        prompt = f"Resume en máximo 2 frases el contenido de este documento:\n\n{content[:1500]}"

        print(f"   Analizando {len(content[:1500])} caracteres...")

        # Usar el método generate_oai_reply de AutoGen
        messages = [{"role": "user", "content": prompt}]
        response = self.generate_oai_reply(messages)

        # extract text from response tuple
        if isinstance(response, tuple):
            response = response[1] if len(response) > 1 else response[0]

        return response if response else "No se pudo analizar el contenido."
