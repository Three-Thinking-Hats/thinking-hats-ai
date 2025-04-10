from langchain.agents import AgentType, initialize_agent
from langchain_openai import ChatOpenAI

from thinking_hats_ai.hats.hats import Hat, Hats
from thinking_hats_ai.prompting_techniques.base_technique import (
    BasePromptingTechnique,
)
from thinking_hats_ai.tools.tools import get_tools_for_hat

from ..utils.api_handler import APIHandler
from ..utils.brainstorming_input import BrainstormingInput
from ..utils.string_utils import list_to_bulleted_string


class ReAct(BasePromptingTechnique):
    def execute_prompt(
        self,
        brainstorming_input: BrainstormingInput,
        hat: Hat,
        api_handler: APIHandler,
    ):
        HAT_TOOL_USE = {
            "Black": "Use the sentimentlimiter to check if your contribution matches the sentiment needed for the hat.",
            "Blue": "Use the ThinkingProcessRater to ckeck if your contribution thinking process management is sufficient for your hat ",
            "Green": "Use the creativity scorer to check if the creativity score matches your hat. ",
            "Red": "Use the sentimentlimiter to check if your contribution matches the sentiment needed for the hat. Use the RedHatClassifier to check if you understood the red hat correctly.",
            "White": "Use the sentimentlimiter to check if your contribution matches the sentiment needed for the hat.",
            "Yellow": "Use the sentimentlimiter to check if your contribution matches the sentiment needed for the hat.",
        }
        input_str = (
            f"Imagine you wear a thinking hat, which leads your thoughts with the following instructions: {Hats().get_instructions(hat)} "
            f"This is the question that was asked for the brainstorming: {brainstorming_input.question} "
            f"These are the currently developed ideas in the brainstorming: {list_to_bulleted_string(brainstorming_input.ideas)} "
            f"What would you add from the perspective of the given hat?  "
            f"{HAT_TOOL_USE[hat.value]}"
            f"Use the hat validator to check if your contribution is correctly classifed as the right hat. "
            f"If all the checks pass you are fine to ouput if one fails rethink your contribution."
            f"Your final response should have the lenght of {brainstorming_input.response_length}"
        )

        llm = ChatOpenAI(
            temperature=0.0,
            model_name="gpt-4o-mini",
            api_key=api_handler.api_key,
        )

        tools = get_tools_for_hat(hat.value, llm)

        agent = initialize_agent(
            tools=tools,
            llm=llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )
        prompt = {"input": input_str}
        response = agent.invoke(prompt)

        self.logger.start_logger(hat.value)
        self.logger.log_prompt(input_str)
        self.logger.log_response(response["output"])
        return response
