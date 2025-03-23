import importlib
import os

from dotenv import load_dotenv

from thinking_hats_ai.hats.hats import Hat, Hats
from thinking_hats_ai.prompting_techniques.technique import Technique
from thinking_hats_ai.utils.api_handler import APIHandler
from thinking_hats_ai.utils.brainstorming_input import BrainstormingInput


class BrainstormingSession:
    def __init__(self, api_key=None, dev=False):
        self.api_key = api_key or self._load_api_key()
        self.api_handler = APIHandler(api_key)
        self.dev = dev

    def generate_idea(self, technique: Technique, hat: Hat, brainstorming_input: BrainstormingInput):
        hat_instructions = Hats().get_instructions(hat)

        try:
            module_name = (
                f"thinking_hats_ai.prompting_techniques.{technique.value}"
            )
            module = importlib.import_module(module_name)
            class_name = technique.value.title().replace("_", "")
            technique_class = getattr(module, class_name)
            technique_instance = technique_class(self.dev)
        except (ModuleNotFoundError, AttributeError) as e:
            raise ValueError(f"Unsupported technique: {technique}") from e

        response = technique_instance.execute_prompt(
            brainstorming_input, hat_instructions, self.api_handler
        )

        return response

    def _load_api_key(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "API key is missing. Please provide an API key when initializing "
                "BrainstormingSession or set 'OPENAI_API_KEY' in the environment variables."
            )
        return api_key
