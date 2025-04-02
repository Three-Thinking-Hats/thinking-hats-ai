import os

from langchain.agents import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain.chat_models import ChatOpenAI
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from thinking_hats_ai.prompting_techniques.base_technique import (
    BasePromptingTechnique,
)

from ..utils.api_handler import APIHandler
from ..utils.brainstorming_input import BrainstormingInput
from ..utils.string_utils import list_to_bulleted_string


class ReAct(BasePromptingTechnique):
    def execute_prompt(
        self,
        brainstorming_input: BrainstormingInput,
        hat_instructions: str,
        api_handler: APIHandler,
    ):
        input_str = (
            f"You are wearing a thinking hat of color: {'Blue'}.\n"
            "The color of the hat determines your perspective, responsibilities, and the way you think."
            "in the ReAct phase you should find out what your color hat does. You should follow the react protocol."
            "Your final answer should be your contribution to the brainstorming session throught the perspective of your hat.\n"
            "Your job is to contribute to the brainstorming based on your hat's perspective.\n\n"
            f"Brainstorming Question: {brainstorming_input.question}\n\n"
            f"Current Ideas:\n{list_to_bulleted_string(brainstorming_input.ideas)}\n\n"
            f"Your task: From the {'Blue'} HAT perspective, suggest what else could be added.\n"
            f"Your response should be approximately {brainstorming_input.response_length} sentences long."
        )

        api_key = os.getenv("OPENAI_API_KEY")
        llm = llm = ChatOpenAI(
            temperature=0, model_name="gpt-4o-mini", openai_api_key=api_key
        )
        api_wrapper = WikipediaAPIWrapper(
            top_k_results=1, doc_content_chars_max=100
        )
        tool = WikipediaQueryRun(api_wrapper=api_wrapper)
        tools = [tool]
        agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )
        prompt = {"input": input_str}
        response = agent.invoke(prompt)

        self.logger.log_response(response)
        return response
