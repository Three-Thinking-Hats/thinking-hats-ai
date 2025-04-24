from langchain.tools import Tool


def get_white_hat_tools(llm):
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
            description="Analyzes if the contribution to the brainstorming is a good or bad white hat respones. It gives tips if it is bad.",
        )
    ]
