import importlib

from thinking_hats_ai.hats.hats import Hat, Hats
from thinking_hats_ai.prompting_techniques.technique import Technique
from thinking_hats_ai.utils.api_handler import APIHandler


class BrainstormingSession:
    def __init__(self, api_key):
        self.api_handler = APIHandler(api_key)

    def generate_idea(self, technique: Technique, hat: Hat, input_text: str):
        hat_instructions = Hats().get_instructions(hat)

        try:
            module_name = (
                f"thinking_hats_ai.prompting_techniques.{technique.value}"
            )
            module = importlib.import_module(module_name)
            class_name = technique.value.title().replace("_", "")
            technique_class = getattr(module, class_name)
            technique_instance = technique_class()
        except (ModuleNotFoundError, AttributeError) as e:
            raise ValueError(f"Unsupported technique: {technique}") from e

        response = technique_instance.execute_prompt(
            input_text, hat_instructions, self.api_handler
        )

        return response
