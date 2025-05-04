from langchain.tools import Tool


def get_green_hat_tools(llm):
    def creativity_analyzer(input_text: str):
        prompt = f"""
            You are a Creativity Analyzer.

            Your task is to assess whether a new idea in a brainstorming session is sufficiently creative and diverse, based on the ideas that have already been contributed.

            Creative ideas should be:
            - Original or unexpected
            - Clearly different from existing ideas
            - Offering a new angle or perspective
            - More than just small variations

            You will receive:
            1. A list of existing ideas
            2. A new idea to evaluate

            Determine whether the new idea introduces **enough novelty** to justify including it. Be strict. Is this idea really creative? If the idea is creative and distinct, respond with:

            ACCEPTED - <short reason>

            If it is too similar, conventional, or unoriginal, respond with:

            REJECTED - <short reason and a tip for improvement>

            Return only one line.

            ---

            Input:
            "{input_text}"

            Creativity Assessment:
                """
        response = llm.invoke(prompt)
        result = response.content.strip()
        print(f"Raw LLM response: {result}")

        if result.startswith("ACCEPTED"):
            return f"🟢 Accepted: {result}\n{input_text}"
        elif result.startswith("REJECTED"):
            return f"🔴 Rejected: {result}\n{input_text}"
        else:
            return "⚠️ Could not determine creativity assessment."

    return [
        Tool(
            name="CreativityAnalyzer",
            func=creativity_analyzer,
            description=(
                "Use this tool to check if a new idea is creative enough. "
                "Format the input as follows:\n"
                '"""\n'
                "Existing Ideas:\n- idea 1\n- idea 2\n...\n\n"
                "New Idea:\n<your idea>\n"
                '"""\n'
                "Make sure you pass both the existing ideas and your new idea clearly."
            ),
        ),
    ]
