from abc import ABC, abstractmethod

from ..utils.logger import Logger


class BasePromptingTechnique(ABC):
    def __init__(self, dev):
        technique_name = self.__class__.__name__.lower()
        self.logger = Logger(technique_name, dev)

    @abstractmethod
    def execute_prompt(self, input_text, hat_instructions):
        pass
