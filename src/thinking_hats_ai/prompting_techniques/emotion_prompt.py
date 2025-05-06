from langchain.prompts import PromptTemplate

from thinking_hats_ai.hats.hats import Hat, Hats
from thinking_hats_ai.prompting_techniques.base_technique import (
    BasePromptingTechnique,
)

from ..utils.api_handler import APIHandler
from ..utils.brainstorming_input import BrainstormingInput
from ..utils.string_utils import list_to_bulleted_string


class EmotionPrompt(BasePromptingTechnique):
    """
    A prompting technique that adds emotional motivation to the reasoning process
    to simulate emotionally influenced decision-making in brainstorming.

    This method injects emotion-based phrases into the prompt to subtly guide
    the model's thinking in alignment with a given hat's perspective.
    """

    def execute_prompt(
        self,
        brainstorming_input: BrainstormingInput,
        hat: Hat,
        api_handler: APIHandler,
    ):
        """
        Executes an emotionally motivated prompt using a specific thinking hat perspective.

        This method enhances the prompt with a predefined motivational phrase, helping the
        model generate more emotionally resonant responses without deviating from the hat style.

        Args:
            brainstorming_input (BrainstormingInput): The brainstorming session question, ideas, and desired response length.
            hat (Hat): The thinking hat perspective to use.
            api_handler (APIHandler): API interface for sending prompts and receiving responses.

        Returns:
            str: The emotionally guided brainstorming contribution.
        """
        emotion_prompts = {
            "ep03": "This is very important to my career",
            "ep09": "Stay focused and dedicated to your goals. Your consistent efforts will lead to outstanding achievements.",
            "ep10": "Take pride in your work and give it your best. Your commitment to excellence sets you apart.",
        }
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
            "What would you add from the perspective of the given hat? {emotion_prompt}\n"
            "Please provide a response that is {length} long.",
        )

        prompt = template.format(
            hat_instructions=Hats().get_instructions(hat),
            question=brainstorming_input.question,
            ideas=list_to_bulleted_string(brainstorming_input.ideas),
            emotion_prompt=emotion_prompts["ep03"],
            length=brainstorming_input.response_length,
        )

        response = api_handler.get_response(prompt)

        self.logger.start_logger(hat.value)
        self.logger.log_prompt(prompt)
        response = api_handler.get_response(prompt)
        self.logger.log_response(response)
        return response
