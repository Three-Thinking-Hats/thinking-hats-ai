from langchain.prompts import PromptTemplate

from thinking_hats_ai.prompting_techniques.base_technique import (
    BasePromptingTechnique,
)

from ..utils.api_handler import APIHandler
from ..utils.brainstorming_input import BrainstormingInput
from ..utils.string_utils import list_to_bulleted_string


class TakeAStepBack(BasePromptingTechnique):
    def execute_prompt(
        self,
        brainstorming_input: BrainstormingInput,
        hat_instructions: str,
        api_handler: APIHandler,
    ):
        template = PromptTemplate(
            input_variables=[
                "hat_instructions",
                "question",
                "ideas",
                "emotion",
                "length",
            ],
            template="Imagine you wear a thinking hat, which leads your thoughts with the following instructions: {hat_instructions}\n"
            "This is the question that was asked for the brainstorming: {question}\n"
            "These are the currently developed ideas in the brainstorming:\n{ideas}\n"
            "What would you add from the perspective of the given hat?\n"
            "{step_back_question}"
            "Please provide a response that is {length} long.",
        )

        step_back_question = (
            "Before adding a new idea, "
            "take a step back and reflect: Are there any gaps, assumptions, "
            "or patterns in the current set of ideas that might limit creative "
            "thinking? What perspective might be missing or underrepresented given "
            "the current brainstorming and the hat's viewpoint?"
        )

        prompt = template.format(
            hat_instructions=hat_instructions,
            question=brainstorming_input.question,
            ideas=list_to_bulleted_string(brainstorming_input.ideas),
            step_back_question=step_back_question,
            length=brainstorming_input.response_length,
        )

        self.logger.log_prompt(prompt, "self_monitoring")

        response = api_handler.get_response(prompt)

        self.logger.log_response(response)

        return response
