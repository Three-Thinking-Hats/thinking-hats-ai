from langchain.prompts import PromptTemplate

from thinking_hats_ai.hats.hats import Hat, Hats
from thinking_hats_ai.prompting_techniques.base_technique import (
    BasePromptingTechnique,
)

from ..utils.api_handler import APIHandler
from ..utils.brainstorming_input import BrainstormingInput
from ..utils.string_utils import list_to_bulleted_string


class PersonaPattern(BasePromptingTechnique):
    """
    A prompting technique where the model adopts the persona of a participant
    embodying the mindset of a specific thinking hat in a brainstorming session.

    This approach emphasizes roleplay and immersive, in-character contribution
    based on the assigned hat's principles without explicitly stating the perspective.
    """

    def execute_prompt(
        self,
        brainstorming_input: BrainstormingInput,
        hat: Hat,
        api_handler: APIHandler,
    ):
        """
        Executes the persona-style prompting process.

        Formats a prompt that asks the language model to take on the persona of a
        brainstorming participant acting under a specific thinking hat's mindset,
        and contribute naturally and contextually to the session.

        Args:
            brainstorming_input (BrainstormingInput): The session's main question, current ideas, and response length.
            hat (Hat): The thinking hat being emulated in persona.
            api_handler (APIHandler): Used to call the language model.

        Returns:
            str: The generated brainstorming contribution, written in the voice of a participant.
        """
        brainstorming_input.question
        template = PromptTemplate(
            input_variables=[
                "hat_instructions",
                "question",
                "ideas",
                "length",
            ],
            template="You are a proactive and insightful contributor in our brainstorming session."
            "Your role is to embody the unique characteristics assigned to you later, based on Edward de Bono's thinking hat methodology."
            "Bring your perspective fully into the discussion, focusing on the principles and mindset linked to your designated hat."
            "Engage with enthusiasm, challenge ideas constructively, and expand on concepts using the approach that aligns with your persona's assigned 'thinking hat."
            "Assigned thinking hat instructions: {hat_instructions}\n"
            "Make your response look like it came from a participant in a brainstorming session and adapt to the writing style of the generated ideas"
            "Do not tell what perspective you are writing from, but make it clear from the content of your response."
            "This is the question that was asked for the brainstorming: {question}\n"
            "These are the currently developed ideas in the brainstorming:\n{ideas}\n"
            "What would you add from the perspective of the given persona?\n"
            "Please provide a response that is {length} long.",
        )

        prompt = template.format(
            hat_instructions=Hats().get_instructions(hat),
            question=brainstorming_input.question,
            ideas=list_to_bulleted_string(brainstorming_input.ideas),
            length=brainstorming_input.response_length,
        )

        self.logger.start_logger(hat.value)

        self.logger.log_prompt(prompt)

        response = api_handler.get_response(prompt)

        self.logger.log_response(response)

        return response
