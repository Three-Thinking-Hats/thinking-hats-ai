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
            "Black": "Use the BlackHatCritiqueRater to check whether your contribution identifies potential risks or downsides clearly and aligns with the critical thinking expected from the Black Hat.",
            "Blue": "Use the BlueHatResponseRater to ckeck if your contribution is a good blue hat contribution to the brainstortming. ",
            "Green": "Use the CreativityAnalyzer to check if the idea is creative enough. Pass all the ideas already generated in the brainstorming question to the creativity analyzer. Make it clear which are the ideas from the brainstorming and which one is your idea.",
            "Red": "Use the FeelingsAssesor to check if you understood the red hat correctly and grounded your contribution in feeling.",
            "White": "Use the WhiteHatAssesor to check if your contribution matches the white hat thinking style",
            "Yellow": "Use the YellowHatValueRater to check whether your contribution highlights specific benefits, value opportunities, or positive impacts as expected from the Yellow Hat.",
        }

        TEMPERATURES = {
            "Black": 0.3,
            "Blue": 0,
            "Green": 1,
            "Red": 0.9,
            "White": 0,
            "Yellow": 0.6,
        }

        input_str = (
            f"Imagine you wear a thinking hat, which leads your thoughts with the following instructions: {Hats().get_instructions(hat)} "
            f"This is the question that was asked for the brainstorming: {brainstorming_input.question} "
            f"These are the currently developed ideas in the brainstorming: {list_to_bulleted_string(brainstorming_input.ideas)} "
            f"What would you add from the perspective of the given hat?  "
            f"{HAT_TOOL_USE[hat.value]}"
            f"Use the hat validator to check if your contribution is correctly classifed as the right hat. If you have the hat validator as a tool."
            f"You should formulate a contribution for the given hat ({hat.value}) and refine it using the tools."
            f"If all the checks pass (you should use all the tools) you are fine to ouput your refined contribution to the brainstorming. If one fails rethink and refine your contribution."
            f"In the end, your Final Answer must be a clean, standalone contribution that fits into the brainstorming session. Do not narrate your reasoning. Do not include thoughts, explanations, or summaries of the tool's ratings. Only return the final, polished contribution as if you were submitting it directly to the group."
            f"Your final answer must begin with 'Final Answer:' and include only your polished contribution to the brainstorming. The recommendation should come from you. Your are not advising anyone on the contribution you make the contribution."
            f"Your final response should have the lenght of {brainstorming_input.response_length}"
        )

        llm_tool = ChatOpenAI(
            temperature=0.0,
            model_name="gpt-4.1",
            api_key=api_handler.api_key,
        )

        llm_agent = ChatOpenAI(
            temperature=TEMPERATURES[hat.value],
            model_name="gpt-4.1",
            api_key=api_handler.api_key,
        )

        tools = get_tools_for_hat(hat.value, llm_tool)

        agent = initialize_agent(
            tools=tools,
            llm=llm_agent,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            handle_parsing_errors=True,
        )
        prompt = {"input": input_str}
        response = agent.invoke(prompt)

        self.logger.start_logger(hat.value)
        self.logger.log_prompt(input_str)
        self.logger.log_response(response["output"])
        return response["output"]
