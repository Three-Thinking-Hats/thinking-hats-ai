from langchain.prompts import PromptTemplate

from thinking_hats_ai.hats.hats import Hat, Hats
from thinking_hats_ai.prompting_techniques.base_technique import (
    BasePromptingTechnique,
)

from ..utils.api_handler import APIHandler
from ..utils.brainstorming_input import BrainstormingInput
from ..utils.string_utils import list_to_bulleted_string


class ContrastivePrompting(BasePromptingTechnique):
    def execute_prompt(
        self,
        brainstorming_input: BrainstormingInput,
        hat: Hat,
        api_handler: APIHandler,
    ):
        brainstorming_input.question
        template = PromptTemplate(
            input_variables=[
                "hat_instructions",
                "question",
                "ideas",
                "length",
            ],
            template="Imagine you are wearing a hat with the following instructions: {hat_instructions}\n"
            "This is the brainstorming question: {question}\n"
            "Here are the currently developed ideas:\n{ideas}\n"

            "Contrastive Example:\n"
            "For example, imagine you received a persona like 'you always want to be realistic' for the question 'How can we make a cool birthday party for friends?' Consider these ideas: ['make a karaoke bar', 'have some pizza', 'make a huge party with 10,000 visitors in the White House'].\n"
            "- A GOOD Response might be: 'Let's host a cozy, realistically planned barbeque party at a friend's house.'\n"
            "- A BAD Response might be: 'Let's throw a huge, impractical party in the White House.\n'"
            "- A BAD Response might be: 'I am always realistic, a party in the white house isn't possible\n'"
            "In this example, the good response aligns with the realistic persona while the bad response ignores context and feasibility. Keep this contrast in mind.\n"

            "Your Task: "
            "Using the perspective defined by your current hat, analyze the provided ideas.\n"
            "First, identify if any of the ideas resemble a “bad response” that contradicts your persona’s instructions.\n"
            "Explain step-by-step why such ideas are problematic, contrasting them with what would be acceptable or desirable.\n"
            "Finally, propose a revised idea or additional insight that better aligns with your persona’s objectives.\n"
            "Your response should be {length} long.\n"
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
