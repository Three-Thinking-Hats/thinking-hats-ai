from langchain.prompts import PromptTemplate

from thinking_hats_ai.hats.hats import Hat, Hats
from thinking_hats_ai.prompting_techniques.base_technique import (
    BasePromptingTechnique,
)

from ..utils.api_handler import APIHandler
from ..utils.brainstorming_input import BrainstormingInput
from ..utils.string_utils import list_to_bulleted_string


class ChainOfVerification(BasePromptingTechnique):
    """
    A prompting technique that validates the quality of a brainstorming idea
    through a multi-step verification process aligned with a specific thinking hat.

    The process generates an idea, plans verification questions, checks alignment
    against those questions, and optionally refines the idea if verification fails.
    """

    def execute_prompt(
        self,
        brainstorming_input: BrainstormingInput,
        hat: Hat,
        api_handler: APIHandler,
    ):
        """
        Executes a chain-of-verification to ensure a hat-aligned contribution.

        Steps:
        1. Generates an initial idea using the provided hat instructions.
        2. Creates five yes/no verification questions to test alignment with the hat's intent.
        3. Verifies the idea by attempting to answer all questions affirmatively.
        4. If the idea passes, returns it as-is.
        5. If any question fails, refines the idea based on the failure reasoning.

        Args:
            brainstorming_input (BrainstormingInput): Contains the brainstorming question, prior ideas, and response length.
            hat (Hat): The thinking hat whose perspective is being simulated.
            api_handler (APIHandler): Interface for communicating with the language model.

        Returns:
            str: A validated or refined brainstorming contribution.
        """
        ### 1. Call -> Generate Idea
        brainstorming_input.question
        template = PromptTemplate(
            input_variables=[
                "hat_instructions",
                "question",
                "ideas",
                "length",
            ],
            template="Imagine you wear a thinking hat, which leads your thoughts with the following instructions: {hat_instructions}\n"
            "This is the question that was asked for the brainstorming: {question}\n"
            "These are the currently developed ideas in the brainstorming:\n{ideas}\n"
            "Propose a contribution for the brainstorming while adhering to your hat.\n"
            "Please provide a response that is {length} long.",
        )

        prompt1 = template.format(
            hat_instructions=Hats().get_instructions(hat),
            question=brainstorming_input.question,
            ideas=list_to_bulleted_string(brainstorming_input.ideas),
            length=brainstorming_input.response_length,
        )

        self.logger.start_logger(hat.value)

        self.logger.log_prompt(prompt1, notes="1. Generate Idea")

        response1 = api_handler.get_response(prompt1)

        self.logger.log_response(response1, notes="1. Generated Idea")

        ### 2. Call -> Plan Verification
        template = PromptTemplate(
            input_variables=["response1", "hat_instructions", "question"],
            template="This was the Brainstorming question: {question}\n"
            "The Idea you have to analyse is: {response1}\n"
            "Create 5 YES/NO verification questions to check weither the contribution suits to a person, which is following these instructions while generating the contribution: {hat_instructions}\n"
            "If the verification is successfull, all questions should be answerable with 'YES'\n"
            "Format the questions like '1. Question1 2. Question2 3. Question3 4.Question4 5.Question5'\n"
            "Do not answer the questions! You only generate verification questions",
        )
        prompt2 = template.format(
            hat_instructions=Hats().get_instructions(hat),
            question=brainstorming_input.question,
            response1=response1,
        )

        self.logger.log_prompt(prompt2, notes="2. Plan Verification")

        response2 = api_handler.get_response(prompt2)

        self.logger.log_response(
            response2, notes="2. Generated Verification Questions"
        )

        ### 3. Call -> Execute Verification
        template = PromptTemplate(
            input_variables=[
                "response2",
                "response1",
            ],
            template="There was a Brainstorming and following contribution came up {response1}\n"
            "Use the verification questions and check weither you can answer all of them with 'YES'\n"
            "If all of them are successfull, return 'Verification Successfull' else return for all why they passed or failed\n"
            "Format your answer like this if all passed: 'Verification was Successful 1. PASS (reason) 2. PASS (reason) 3. PASS (reason) 4. PASS (reason) 5. PASS (reason)'\n"
            "Format your answer like this if one or more failed: 'Verification was Failed 1. PASS/FAIL (reason) 2. PASS/FAIL (reason) 3. PASS/FAIL (reason) 4. PASS/FAIL (reason) 5. PASS/FAIL (reason)'\n"
            "Verification questions: {response2}",
        )
        prompt3 = template.format(response1=response1, response2=response2)

        self.logger.log_prompt(prompt3, notes="3. Execute Verification")

        response3 = api_handler.get_response(prompt3)

        self.logger.log_response(response3, notes="3. Executed Verification")

        ### 4. Return contribution if verification was successfull
        if response3.startswith("Verification was Successful"):
            self.logger.log_response(
                response1, notes="4. Final response (not Optimized)"
            )
            return response1

        ### 4. Call -> Optimize contribution
        template = PromptTemplate(
            input_variables=[
                "response1",
                "response2",
                "response3",
                "hat_instructions",
                "length",
            ],
            template="There was a Brainstorming and following idea came up: {response1}\n"
            "This was verified with following verification questions: {response2}\n"
            "Failed questions with reason for failure: {response3}\n"
            "The person creating the contribution had to follow these instructions: {hat_instructions}\n"
            "Change the contribution to resolve the failed verification but to not change the main argument in the contribution\n"
            "Please provide a refined contribution that is {length} long. Do only return a final contribution.",
        )
        prompt4 = template.format(
            hat_instructions=Hats().get_instructions(hat),
            question=brainstorming_input.question,
            length=brainstorming_input.response_length,
            response1=response1,
            response2=response2,
            response3=response3,
        )

        self.logger.log_prompt(prompt4, notes="4. Optimize Contribution")

        response4 = api_handler.get_response(prompt4)

        self.logger.log_response(
            response4, notes="4. Final response (Optimized)"
        )

        return response4
