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
            "Green": "Use the creativity analyzer to check if the idea is creative enough. Pass all the ideas already generated in the brainstorming question to the creativity analyzer. Make it clear which are the ideas from the brainstorming and which one is your idea.",
            "Red": "First us the FlipACoin to determine what mood you are in. Use the sentimentlimiter to check if your contribution matches the sentiment needed for the hat. Use the RedHatClassifier to check if you understood the red hat correctly.",
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
            f"If all the checks pass (you should use all the tools) you are fine to ouput if one fails rethink your contribution."
            f"Your final response should have the lenght of {brainstorming_input.response_length}"
        )

        llm_tool = ChatOpenAI(
            temperature=0.0,
            model_name="gpt-3.5-turbo",
            api_key=api_handler.api_key,
        )

        llm_agent = ChatOpenAI(
            temperature=1.0,
            model_name="gpt-3.5-turbo",
            api_key=api_handler.api_key,
        )

        tools = get_tools_for_hat(hat.value, llm_tool)

        agent = initialize_agent(
            tools=tools,
            llm=llm_agent,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )
        prompt = {"input": input_str}
        response = agent.invoke(prompt)

        self.logger.start_logger(hat.value)
        self.logger.log_prompt(input_str)
        self.logger.log_response(response["output"])
        return response["output"]
