from langchain.prompts import PromptTemplate

from thinking_hats_ai.prompting_techniques.base_technique import (
    BasePromptingTechnique,
)

from ..utils.api_handler import APIHandler
from ..utils.brainstorming_input import BrainstormingInput
from ..utils.string_utils import list_to_bulleted_string


class MultiAgent(BasePromptingTechnique):
    def execute_prompt(
        self,
        brainstorming_input: BrainstormingInput,
        hat_instructions: str,
        api_handler: APIHandler,
    ):
        brainstorming_input.question
        template = PromptTemplate(
            input_variables=[
                "hat_instructions"
            ],
            template= "The task for a multi agent prompt is, to create a contribution to a brainstorming from the point of view of the following persona: {hat_instructions}\n"
            "They will receive a brainstorming question and a list of previously generated ideas, along to the task to create a contribution\n"
            "Your task is, to create personas as for the multi agent. There must be at least 3 personas, which are all different from each other.\n"
            "Return the personas as a json'\n"
        )

        prompt = template.format(
            hat_instructions=hat_instructions,
        )

        self.logger.log_prompt(prompt, notes="META PROMPT - GENERATE PERSONAS")

        response = api_handler.get_response(prompt)

        self.logger.log_response(response, notes="META PROMPT - GENERATED PERSONAS")

        return response
