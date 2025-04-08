from langchain.prompts import PromptTemplate

from thinking_hats_ai.hats.hats import Hat, Hats
from thinking_hats_ai.prompting_techniques.base_technique import (
    BasePromptingTechnique,
)

from ..utils.api_handler import APIHandler
from ..utils.brainstorming_input import BrainstormingInput
from ..utils.string_utils import list_to_bulleted_string


class EmotionPrompt(BasePromptingTechnique):
    def execute_prompt(
        self,
        brainstorming_input: BrainstormingInput,
        hat: Hat,
        api_handler: APIHandler,
    ):
        self_monitoring = "This is very important to my career"
        social_cognitive_theory = "Embrace challenges as opportunities for growth. Each obstacle you overcome brings you closer to success."
        cognitive_emotion_regulation = "You'd better be sure."
        brainstorming_input.question
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
            "What would you add from the perspective of the given hat? {emotion}\n"
            "Please provide a response that is {length} long.",
        )

        prompt = template.format(
            hat_instructions=Hats().get_instructions(hat),
            question=brainstorming_input.question,
            ideas=list_to_bulleted_string(brainstorming_input.ideas),
            emotion=cognitive_emotion_regulation,
            length=brainstorming_input.response_length,
        )

        response = api_handler.get_response(prompt)

        self.logger.start_logger(hat.value)
        self.logger.log_prompt(prompt)
        response = api_handler.get_response(prompt)

        return response
