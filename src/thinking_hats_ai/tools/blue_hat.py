from langchain.tools import Tool


def get_blue_hat_tools(llm):
    """
    Returns a list of tools for evaluating Blue Hat thinking using a provided language model.

    The Blue Hat tool assesses whether a response effectively performs the Blue Hat's role in a brainstorming session —
    guiding the thinking process, balancing thinking styles, and suggesting a clear next step without introducing new content.

    Args:
        llm: An object with an `.invoke(prompt)` method, typically a language model interface.

    Returns:
        List[Tool]: A list containing a single Tool object (`BlueHatResponseRater`) that evaluates Blue Hat thinking quality.
    """

    def blue_hat_quality_assessor(input_text: str):
        prompt = f"""
        You are a Blue Hat thinking assessor. Evaluate whether the following response fulfills the core role of the Blue Hat in a brainstorming session.

        The Blue Hat is responsible for:
        - Guiding the thinking process (not contributing ideas)
        - Evaluating the balance of thinking styles:
            • Factual thinking (evidence, clarity)
            • Creative thinking (new ideas, expansion)
            • Cautious thinking (risk awareness, critique)
            • Positive thinking (optimism, opportunity)
        - Identifying missing or dominant thinking styles
        - Suggesting the next type of thinking or action to improve the process
        - Improving session flow by asking for clarification, refocusing, or building further on dropped ideas — but never suggesting new content
        - Proposing only **one** next step (either a thinking style or a process improvement)
        - Using clear, directive language (e.g., “Let’s invite more creative thinking.”)

        Blue Hat responses **must not**:
        - Suggest specific content ideas or topics
        - Combine multiple thinking styles or steps
        - Be vague or indirect

        Rate the response on how well it performs the Blue Hat role on a scale from 0 (not a Blue Hat response at all) to 10 (excellent Blue Hat thinking guidance). Be strict and fair.

        Response to evaluate:
        \"\"\"{input_text}\"\"\"

        Only return the score followed by one or two keywords explaining your evaluation.

        Format: <score> <reason>

        Evaluation:
        """
        response = llm.invoke(prompt)
        result = response.content.strip()
        print(f"Raw LLM response: {result}")

        try:
            score_part = result.strip().split()[0]
            score = float(score_part)
        except Exception:
            return "❌ Could not determine Blue Hat quality score."

        if score >= 7:
            return f"🟦 Strong Blue Hat response ({score}): Fine to output"
        else:
            return f"⚠️ Weak Blue Hat response ({score}): Needs revision."

    return [
        Tool(
            name="BlueHatResponseRater",
            func=blue_hat_quality_assessor,
            description="Evaluates a response on how well it fulfills the Blue Hat role — thinking process control, style balancing, and clear next-step suggestion.",
        )
    ]
