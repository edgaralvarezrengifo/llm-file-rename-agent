from autogen import AssistantAgent
import PyPDF2, os

class AnalyzerAgent(AssistantAgent):
    def analyze_file(self, file_path):
        content = ""
        if file_path.endswith(".pdf"):
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    content += page.extract_text()
        elif file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = "Tipo de archivo no soportado."

        prompt = f"Analiza el siguiente documento y describe su contenido brevemente:\n\n{content[:3000]}"
        response = self.llm.generate(prompt)
        return response
