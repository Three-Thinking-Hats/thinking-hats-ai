from abc import ABC, abstractmethod

from ..utils.api_handler import APIHandler
from ..utils.brainstorming_input import BrainstormingInput


class BasePromptingTechnique(ABC):
    @abstractmethod
    def execute_prompt(
        self,
        brainstorming_input: BrainstormingInput,
        hat_instructions: str,
        api_handler: APIHandler,
    ):
        pass
