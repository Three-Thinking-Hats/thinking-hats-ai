from abc import ABC, abstractmethod

from thinking_hats_ai.hats.hats import Hat

from ..utils.api_handler import APIHandler
from ..utils.brainstorming_input import BrainstormingInput
from ..utils.logger import Logger


class BasePromptingTechnique(ABC):
    """
    Abstract base class for all prompting techniques used in the thinking hats AI framework.

    Subclasses must implement the `execute_prompt` method to define how a specific prompting
    technique generates a brainstorming contribution based on a selected thinking hat.
    """

    def __init__(self, dev):
        """
        Initializes the logger for the prompting technique.

        Args:
            dev (bool): If True, enables logging to files for development purposes.
        """
        technique_name = self.__class__.__name__.lower()
        self.logger = Logger(technique_name, dev)

    @abstractmethod
    def execute_prompt(
        self,
        brainstorming_input: BrainstormingInput,
        hat: Hat,
        api_handler: APIHandler,
    ):
        """
        Abstract method to execute the prompting technique.

        Args:
            brainstorming_input (BrainstormingInput): Contains the brainstorming question, ideas, and response length.
            hat (Hat): The thinking hat to guide the response style.
            api_handler (APIHandler): Used to interact with the language model.

        Returns:
            str: The generated brainstorming response.
        """
        pass
