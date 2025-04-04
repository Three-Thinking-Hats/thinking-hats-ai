from langchain.prompts import PromptTemplate

from thinking_hats_ai.hats.hats import Hat, Hats
from thinking_hats_ai.prompting_techniques.base_technique import (
    BasePromptingTechnique,
)

from ..utils.api_handler import APIHandler
from ..utils.brainstorming_input import BrainstormingInput
from ..utils.string_utils import list_to_bulleted_string


class FewShot(BasePromptingTechnique):
    def execute_prompt(
        self,
        brainstorming_input: BrainstormingInput,
        hat: Hat,
        api_handler: APIHandler,
    ):
        self.logger.start_logger(hat.value)

        meta_template = PromptTemplate(
            input_variables=["hat_instructions"],
            template=(
                "Imagine you are wearing a thinking hat with the following instructions: {hat_instructions}\n"
                "Generate three concrete examples of how this thinking hat would contribute to a brainstorming session.\n"
                "Your answer must consist of only these two examples and the brainstorming context that was used."
            ),
        )

        meta_prompt = meta_template.format(
            hat_instructions=Hats().get_instructions(hat),
        )
        self.logger.log_prompt(meta_prompt, "Meta Prompt")

        meta_response = api_handler.get_response(meta_prompt)
        self.logger.log_response(meta_response, "Meta Response")

        template = PromptTemplate(
            input_variables=[
                "hat_instructions",
                "question",
                "ideas",
                "length",
                "examples",
            ],
            template="Imagine you wear a thinking hat, which leads your thoughts with the following instructions: {hat_instructions}\n"
            "This is the question that was asked for the current brainstorming session: {question}\n"
            "These are the currently developed ideas in the brainstorming session:\n{ideas}\n\n"
            "Here are some examples of how this thinking hat would respond to other brainstorming questions:\n{examples}\n\n"
            "Now, considering the current question: What would you add from the perspective of the given hat?\n"
            "Please provide a response that is {length} long.",
        )

        prompt = template.format(
            hat_instructions=Hats().get_instructions(hat),
            question=brainstorming_input.question,
            ideas=list_to_bulleted_string(brainstorming_input.ideas),
            length=brainstorming_input.response_length,
            examples=meta_response,
        )
        self.logger.log_prompt(prompt, "Prompt")

        response = api_handler.get_response(prompt)
        self.logger.log_response(response, "Response")

        return response
