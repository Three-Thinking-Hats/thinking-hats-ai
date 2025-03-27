from abc import ABC, abstractmethod

from ..utils.api_handler import APIHandler
from ..utils.brainstorming_input import BrainstormingInput
from ..utils.logger import Logger


class BasePromptingTechnique(ABC):
    def __init__(self, dev):
        technique_name = self.__class__.__name__.lower()
        self.logger = Logger(technique_name, dev)

    @abstractmethod
    def execute_prompt(
        self,
        brainstorming_input: BrainstormingInput,
        hat_instructions: str,
        api_handler: APIHandler,
    ):
        pass
