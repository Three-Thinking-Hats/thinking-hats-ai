from abc import ABC, abstractmethod


class BasePromptingTechnique(ABC):
    @abstractmethod
    def execute_prompt(self, input_text, hat_instructions):
        pass
