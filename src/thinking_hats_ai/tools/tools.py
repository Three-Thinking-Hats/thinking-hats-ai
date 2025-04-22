from langchain.chat_models.base import BaseChatModel
from langchain.tools import Tool

from .black_hat import get_black_hat_tools
from .blue_hat import get_blue_hat_tools
from .green_hat import get_green_hat_tools
from .red_hat import get_red_hat_tools
from .white_hat import get_white_hat_tools
from .yellow_hat import get_yellow_hat_tools


def get_hat_guesser_tool(expected_hat: str, llm: BaseChatModel) -> Tool:
    expected_hat = expected_hat.capitalize()

    def hat_guesser(input_text: str) -> str:
        prompt = f"""
            You are a thinking-hat classifier.
            Based on the content and style of the message below, determine which of the six thinking hats it most closely represents.

            Here are the options:
            - Red Hat:  Emotion, feelings, intuition
            - White Hat: Facts, neutrality, evidence-based reasoning
            - Green Hat: Creativity, new ideas, lateral thinking
            - Yellow Hat: Positivity, benefits, value-focused analysis
            - Black Hat: Caution, critique, risk-awareness
            - Blue Hat: Orchestration, meta-thinking, managing the thinking process

            Text:
            \"\"\"{input_text}\"\"\"

            Only return the hat color (Red, White, Green, Yellow, Black, Blue) and a one-line explanation of why. And how to improve to get to the expected hat color: {expected_hat}
            Example output: Red - This response is based on emotional reasoning but the expected hat was white maybe less emotions are needed.
            Other example output: Green - this responses adds creative suggestions and the expected hat was green so good job."
            """

        response = llm.invoke(prompt)
        result = response.content.strip()

        guessed_hat = result.split()[0].capitalize()

        if guessed_hat == expected_hat:
            return f"✅ Hat match: {guessed_hat}. Accepted.\nExplanation: {result}"
        else:
            return f"❌ Hat mismatch. Expected {expected_hat}, but got {guessed_hat}.\nExplanation: {response}"

    return Tool(
        name="HatValidator",
        func=hat_guesser,
        description=f"Use this tool to check if your contributions matches the correct hat. Validates that a message matches {expected_hat} Hat thinking style",
    )


HAT_TOOL_LOADERS = {
    "Black": get_black_hat_tools,
    "Blue": get_blue_hat_tools,
    "Green": get_green_hat_tools,
    "Red": get_red_hat_tools,
    "White": get_white_hat_tools,
    "Yellow": get_yellow_hat_tools,
}


def get_tools_for_hat(hat_color: str, llm):
    loader = HAT_TOOL_LOADERS.get(hat_color)
    try:
        tools = loader(llm)
    except TypeError:
        tools = []
    tools.append(get_hat_guesser_tool(hat_color, llm))
    return tools
