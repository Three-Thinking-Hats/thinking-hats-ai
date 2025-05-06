from langchain.prompts import PromptTemplate

from thinking_hats_ai.hats.hats import Hat, Hats
from thinking_hats_ai.prompting_techniques.base_technique import (
    BasePromptingTechnique,
)

from ..utils.api_handler import APIHandler
from ..utils.brainstorming_input import BrainstormingInput
from ..utils.string_utils import list_to_bulleted_string


class ZeroShotCot(BasePromptingTechnique):
    """
    A prompting technique that uses a zero-shot chain-of-thought (CoT) strategy
    to simulate a specific thinking hat's mindset when generating brainstorming responses.
    """

    def execute_prompt(
        self,
        brainstorming_input: BrainstormingInput,
        hat: Hat,
        api_handler: APIHandler,
    ):
        """
        Executes a zero-shot chain-of-thought prompt using the specified thinking hat.

        Constructs a context-aware prompt incorporating the thinking hat's instructions,
        the brainstorming question, and existing ideas. Sends it to the language model
        through the provided API handler, logs the interaction, and returns the response.

        Args:
            brainstorming_input (BrainstormingInput): The input question, ideas, and desired response length.
            hat (Hat): The thinking hat perspective to apply.
            api_handler (APIHandler): The handler used to invoke the language model.

        Returns:
            str: The generated response from the language model.
        """
        brainstorming_input.question
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
            "What would you add taking on the perspective of the given hat from the instructions mentioned above? Justify your answer and think step-by-step.\n"
            "Please provide a response that is {length} long.",
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
        response = api_handler.get_response(prompt)
        self.logger.log_response(response)
        return response
