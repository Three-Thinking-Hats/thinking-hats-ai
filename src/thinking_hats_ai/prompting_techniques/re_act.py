from langchain.agents import AgentType, initialize_agent, load_tools
from langchain_openai import ChatOpenAI

from thinking_hats_ai.hats.hats import Hat, Hats
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
        hat: Hat,
        api_handler: APIHandler,
    ):
        input_str = (
            f"Imagine you wear a thinking hat, which leads your thoughts with the following instructions: {Hats().get_instructions(hat)}\n"
            f"This is the question that was asked for the brainstorming: {brainstorming_input.question}\n"
            f"These are the currently developed ideas in the brainstorming:\n{list_to_bulleted_string(brainstorming_input.ideas)}\n"
            f"What would you add from the perspective of the given hat?\n"
        )

        llm = llm = ChatOpenAI(
            temperature=0.8,
            model_name="gpt-4o-mini",
            api_key=api_handler.api_key,
        )

        tools = load_tools(
            ["human"],
            llm=llm,
        )

        agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
        )
        prompt = {"input": input_str}
        response = agent.invoke(prompt)

        self.logger.start_logger(hat.value)
        self.logger.log_prompt(prompt)
        response = api_handler.get_response(prompt)

        return response
