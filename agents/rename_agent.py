from autogen import AssistantAgent
import os, re

class RenameAgent(AssistantAgent):
    def rename_based_on_description(self, original_path, description):
        prompt = f"Genera un nombre de archivo corto y descriptivo en formato snake_case según esta descripción:\n{description}"
        name = self.llm.generate(prompt)
        clean_name = re.sub(r'[^a-zA-Z0-9_]', '', name.strip().lower().replace(" ", "_"))
        extension = os.path.splitext(original_path)[1]
        new_path = os.path.join("data/output", f"{clean_name}{extension}")
        os.rename(original_path, new_path)
        return new_path
