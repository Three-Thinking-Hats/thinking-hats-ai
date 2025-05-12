from langchain.tools import Tool


def get_white_hat_tools(llm):
    """
    Returns a list of tools for evaluating White Hat thinking using a provided language model.

    The returned tool analyzes whether a brainstorming contribution adheres to the White Hat mode of thinking,
    which emphasizes objective, factual, and non-judgmental input.

    Args:
        llm: An object with an `.invoke(prompt)` method, typically a language model interface.

    Returns:
        List[Tool]: A list containing a single Tool object (`WhiteHatAssesor`) that assesses White Hat reasoning.
    """

    def white_hat_assessor(input_text: str):
        prompt = f"""
                You are a White Hat assessor. Your role is to evaluate whether the following brainstorming contribution follows White Hat thinking.

                White Hat thinking is:
                - Neutral and objective
                - Based on facts, data, or known information
                - Focused on clarifying what is known vs. what needs to be known
                - Free of emotion, judgment, or opinion
                - Not speculative or creative

                Please return your assessment in the following format:

                Format:
                <good/bad> - <short reason>
                <improvement tip if bad>

                Evaluate this response:
                \"\"\"{input_text}\"\"\"
                    """

        # Replace with your actual LLM call
        response = llm.invoke(prompt)
        result = response.content.strip()
        print(f"White Hat Assessor Response: {result}")

        return result

    return [
        Tool(
            name="WhiteHatAssesor",
            func=white_hat_assessor,
            description="Analyzes if the contribution to the brainstorming is a good or bad white hat response. It gives tips if it is bad.",
        )
    ]
