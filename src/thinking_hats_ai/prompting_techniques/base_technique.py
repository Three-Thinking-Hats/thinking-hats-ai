from abc import ABC, abstractmethod


class BasePromptingTechnique(ABC):
    @abstractmethod
    def generate_prompt(self, input_text, hat_instructions):
        pass
