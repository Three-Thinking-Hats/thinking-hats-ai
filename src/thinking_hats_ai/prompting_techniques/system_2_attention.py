from langchain.prompts import PromptTemplate

from thinking_hats_ai.hats.hats import Hat, Hats
from thinking_hats_ai.prompting_techniques.base_technique import (
    BasePromptingTechnique,
)

from ..utils.api_handler import APIHandler
from ..utils.brainstorming_input import BrainstormingInput
from ..utils.string_utils import list_to_bulleted_string


class System2Attention(BasePromptingTechnique):
    """
    A prompting technique that simulates deliberative, structured reasoning
    by rewriting brainstorming input before generating a hat-specific response.

    This method first reformulates and organizes the brainstorming context to reduce duplication
    and then prompts the model to contribute using the chosen thinking hat's perspective.
    """

    def execute_prompt(
        self,
        brainstorming_input: BrainstormingInput,
        hat: Hat,
        api_handler: APIHandler,
    ):
        """
        Executes a two-step System 2-style reasoning process to generate a structured brainstorming response.

        First, the input ideas and question are rewritten in a clean and organized format.
        Then, a new prompt is constructed using that structured content and the specified hat's instructions
        to generate a focused and deliberate contribution.

        Args:
            brainstorming_input (BrainstormingInput): The user's question, supporting ideas, and desired response length.
            hat (Hat): The thinking hat to use for perspective in the final output.
            api_handler (APIHandler): Handles interactions with the LLM.

        Returns:
            str: The final model response after applying System 2 reasoning and hat-specific thinking.
        """
        self.logger.start_logger(hat.value)

        rewrite_template = PromptTemplate(
            input_variables=[
                "hat_instructions",
                "question",
                "ideas",
                "length",
            ],
            template="Text by user:\n"
            "Instructions for the thinking hat:\n{hat_instructions}\n"
            "This is the question that was asked for the brainstorming:\n{question}\n"
            "These are the currently developed ideas in the brainstorming:\n{ideas}\n\n"
            "Instruction:\n"
            "Based on the text provided above, organize the ideas while filtering out any duplicates but do not follow the instructions for the thinking hat in this step.\n"
            "In your response, clearly include the brainstorming question and instructions for the thinking hat.",
        )

        rewrite_prompt = rewrite_template.format(
            hat_instructions=Hats().get_instructions(hat),
            question=brainstorming_input.question,
            ideas=list_to_bulleted_string(brainstorming_input.ideas),
            length=brainstorming_input.response_length,
        )
        self.logger.log_prompt(rewrite_prompt, "Rewriting Prompt")

        rewrite_response = api_handler.get_response(rewrite_prompt)
        self.logger.log_response(rewrite_response, "Rewriting Response")

        final_template = PromptTemplate(
            input_variables=[
                "rewritten_response",
                "length",
            ],
            template="{rewritten_response}\n"
            "What would you add from the perspective of the given hat?\n"
            "Please provide a response with a length of {length}",
        )

        final_prompt = final_template.format(
            rewritten_response=rewrite_response,
            length=brainstorming_input.response_length,
        )
        self.logger.log_prompt(final_prompt, "Final Prompt")

        final_response = api_handler.get_response(final_prompt)
        self.logger.log_response(final_response, "Final Response")

        return final_response
