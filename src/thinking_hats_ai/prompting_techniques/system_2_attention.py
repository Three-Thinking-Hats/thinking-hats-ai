from langchain.prompts import PromptTemplate

from thinking_hats_ai.prompting_techniques.base_technique import (
    BasePromptingTechnique,
)

from ..utils.api_handler import APIHandler
from ..utils.brainstorming_input import BrainstormingInput
from ..utils.string_utils import list_to_bulleted_string


class System2Attention(BasePromptingTechnique):
    def execute_prompt(
        self,
        brainstorming_input: BrainstormingInput,
        hat_instructions: str,
        api_handler: APIHandler,
    ):
        rewrite_template = PromptTemplate(
            input_variables=[
                "hat_instructions",
                "question",
                "ideas",
                "length",
            ],
            template="Given the following text by a user, extract the part that is actually relevant to the task that is given. Please also include the actual task or query that the user is asking\n."
            "Text by user:\n"
            "Imagine you are wearing a 'thinking hat' that guides your reasoning style with the following instructions: {hat_instructions}\n"
            "This is the question that was asked for the brainstorming: {question}\n"
            "These are the currently developed ideas in the brainstorming:\n{ideas}\n"
            "What would you add from the perspective of the given hat?",
        )

        rewrite_prompt = rewrite_template.format(
            hat_instructions=hat_instructions,
            question=brainstorming_input.question,
            ideas=list_to_bulleted_string(brainstorming_input.ideas),
            length=brainstorming_input.response_length,
        )

        self.logger.log_prompt(rewrite_prompt)

        rewrite_response = api_handler.get_response(rewrite_prompt)

        self.logger.log_response(rewrite_response)

        final_template = PromptTemplate(
            input_variables=[
                "rewritten_response",
                "length",
            ],
            template="{rewritten_response}\n"
            "Please provide a response that is {length} long.",
        )

        final_prompt = final_template.format(
            rewritten_response=rewrite_response,
            length=brainstorming_input.response_length,
        )

        self.logger.log_prompt(final_prompt)

        final_response = api_handler.get_response(final_prompt)

        self.logger.log_response(final_response)

        return final_response
