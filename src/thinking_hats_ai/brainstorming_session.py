"""
Defines the BrainstormingSession class, which orchestrates idea generation using
different prompting techniques and thinking hats.

Responsibilities:
- Dynamically loads the appropriate prompting technique.
- Invokes the technique with the selected thinking hat and input.
- Manages API key handling for LLM interactions.
"""

import importlib
import os

from dotenv import load_dotenv

from thinking_hats_ai.hats.hats import Hat
from thinking_hats_ai.prompting_techniques.technique import Technique
from thinking_hats_ai.utils.api_handler import APIHandler
from thinking_hats_ai.utils.brainstorming_input import BrainstormingInput


class BrainstormingSession:
    """
    Manages the execution of brainstorming techniques using specific thinking hats.

    Handles API setup, dynamic technique loading, and input execution
    to produce an LLM-generated brainstorming contribution.
    """

    def __init__(self, api_key=None, dev=False):
        """
        Initializes a BrainstormingSession with an API key and development mode flag.

        Args:
            api_key (str, optional): OpenAI API key. Defaults to environment variable if not provided.
            dev (bool): Enables verbose logging if True. Defaults to False.
        """
        self.api_key = api_key or self._load_api_key()
        self.api_handler = APIHandler(api_key)
        self.dev = dev

    def generate_idea(
        self,
        technique: Technique,
        hat: Hat,
        brainstorming_input: BrainstormingInput,
    ):
        """
        Executes the selected prompting technique using the specified hat and input.

        Dynamically loads the correct module and class based on the Technique enum,
        then runs the `execute_prompt` method with the provided brainstorming input.

        Args:
            technique (Technique): The prompting technique to use.
            hat (Hat): The thinking hat perspective to apply.
            brainstorming_input (BrainstormingInput): Contains question, ideas, and desired response length.

        Returns:
            str: The LLM-generated brainstorming contribution.
        """
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
            brainstorming_input, hat, self.api_handler
        )

        return response

    def _load_api_key(self):
        """
        Loads the OpenAI API key from the environment (.env) file.

        Returns:
            str: The API key.

        Raises:
            ValueError: If the key is missing from both args and environment.
        """
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "API key is missing. Please provide an API key when initializing "
                "BrainstormingSession or set 'OPENAI_API_KEY' in the environment variables."
            )
        return api_key
