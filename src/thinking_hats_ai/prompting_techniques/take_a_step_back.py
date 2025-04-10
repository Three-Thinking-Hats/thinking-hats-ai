from langchain.prompts import PromptTemplate

from thinking_hats_ai.hats.hats import Hat, Hats
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
        hat: Hat,
        api_handler: APIHandler,
    ):
        hat_instruction = Hats().get_instructions(hat)
        step_back_template = PromptTemplate(
            input_variables=["hat_color", "hat_imnstructions"],
            template="I wan't to use the take-a-step-back prompting technique. Here is a quick explanation of this prompting technique: "
            "Instead of jumping straight to a solution the step-back-question"
            "should ask the model to pause and reflect on the problem as a whole, break it down into smaller parts or reassess the approach. "
            "It should start with lets-take a step back and..."
            "Please formulate a step-back question for the hat with following instruction {hat_instructions}. "
            "You are not contributing to a brainstorming session. "
            "But the step-back-question is used to prompt chat-GPT to contribute to a brainstorming session using the above instructions.",
        )

        step_back_prompt = step_back_template.format(
            hat_color=hat.value, hat_instructions=hat_instruction
        )

        step_back_question = api_handler.get_response(step_back_prompt)

        template = PromptTemplate(
            input_variables=[
                "hat_instructions",
                "question",
                "ideas",
                "step_back_question",
                "length",
            ],
            template="Imagine you wear a thinking hat, which leads your thoughts with the following instructions: {hat_instructions}\n"
            "This is the question that was asked for the brainstorming: {question}\n"
            "These are the currently developed ideas in the brainstorming:\n{ideas}\n"
            "What would you add from the perspective of the given hat?\n"
            "{step_back_question} "
            "The step-back-question should not be mentioned in the response it should only motivate you to think about the topic. "
            "Please provide a response that is {length} long. "
            "In your response only contributions to the brainstorming session should be included. ",
        )

        prompt = template.format(
            hat_instructions=hat_instruction,
            question=brainstorming_input.question,
            ideas=list_to_bulleted_string(brainstorming_input.ideas),
            step_back_question=step_back_question,
            length=brainstorming_input.response_length,
        )
        self.logger.start_logger(hat.value)
        self.logger.log_prompt(step_back_prompt)
        self.logger.log_response(step_back_question, "step_back_question")
        self.logger.log_prompt(prompt)
        response = api_handler.get_response(prompt)

        self.logger.log_response(response)

        return response
