from langchain.prompts import PromptTemplate

from thinking_hats_ai.hats.hats import Hat, Hats
from thinking_hats_ai.prompting_techniques.base_technique import (
    BasePromptingTechnique,
)

from ..utils.api_handler import APIHandler
from ..utils.brainstorming_input import BrainstormingInput
from ..utils.string_utils import list_to_bulleted_string


class ChainOfThought(BasePromptingTechnique):
    """
    A prompting technique that simulates chain-of-thought reasoning from the perspective
    of a selected thinking hat.

    This method encourages step-by-step thinking by guiding the model with detailed
    hat instructions and temporarily switches to the o3-mini model to apply reasoning.
    """

    def execute_prompt(
        self,
        brainstorming_input: BrainstormingInput,
        hat: Hat,
        api_handler: APIHandler,
    ):
        """
        Executes a chain-of-thought prompt aligned with a specific thinking hat perspective.

        The process temporarily swaps the LLM to a faster model, builds a detailed prompt,
        collects the response, logs everything, and then restores the original model.

        Args:
            brainstorming_input (BrainstormingInput): The session input including question, ideas, and response length.
            hat (Hat): The thinking hat to simulate.
            api_handler (APIHandler): Handles interaction with the language model.

        Returns:
            str: The brainstorming contribution generated using chain-of-thought reasoning.
        """

        original_model = api_handler.chat_model.model_name
        api_handler.change_model("o3-mini")
        template = PromptTemplate(
            input_variables=[
                "hat_instructions",
                "question",
                "ideas",
                "length",
            ],
            template="Imagine you wear a thinking hat, which leads your thoughts with the following instructions: {hat_instructions}\n"
            "This is the question that was asked for the brainstorming: {question}\n"
            "These are the currently developed ideas in the brainstorming:\n{ideas}\n"
            "What would you add from the perspective of the given hat?\n"
            "Please provide a response with a length of {length}",
        )

        prompt = template.format(
            hat_instructions=Hats().get_instructions(hat),
            question=brainstorming_input.question,
            ideas=list_to_bulleted_string(brainstorming_input.ideas),
            length=brainstorming_input.response_length,
        )
        response = api_handler.get_response(prompt)

        self.logger.start_logger(hat.value)
        self.logger.log_prompt(prompt)
        self.logger.log_response(response)

        api_handler.change_model(original_model)

        return response
