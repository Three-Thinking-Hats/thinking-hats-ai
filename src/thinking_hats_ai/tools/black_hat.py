from langchain.tools import Tool


def get_black_hat_tools(llm):
    """
    Returns a list of tools for evaluating Black Hat thinking using a provided language model.

    The tool assesses whether a response demonstrates strong, risk-aware critical thinking as expected from
    the Black Hat role in the Six Thinking Hats method — including identifying specific dangers and naming
    types of risk in a constructive, cautionary manner.

    Args:
        llm: An object with an `.invoke(prompt)` method, typically a language model interface.

    Returns:
        List[Tool]: A list containing a single Tool object (`BlackHatCritiqueRater`) that evaluates critical thinking.
    """

    def black_hat_critique_rater(input_text: str):
        prompt = f"""
        You are a Black Hat assessor. Your task is to evaluate whether the following response demonstrates **strong risk-focused critical thinking** as expected from the Black Hat in a brainstorming session.

        A proper Black Hat response should:
        - Identify potential **dangers or downsides** of ideas
        - Specify the **type of risk** (e.g., safety, legal, financial, ethical, reputational, long-term impact)
        - Refer to parts of specific ideas or patterns in the brainstorming
        - Avoid vague negativity or personal opinion
        - Offer **constructive caution**, not just rejection

        Rate how well the following response meets these criteria on a scale from 0 to 10.

        Response to evaluate:
        \"\"\"{input_text}\"\"\"

        Only return the score followed by a one- or two-word explanation.

        Format: <score> <reason>

        Risk Analysis Score:
        """
        response = llm.invoke(prompt)
        result = response.content.strip()
        print(f"Raw LLM response: {result}")
        try:
            score_part = result.strip().split()[0]
            score = float(score_part)
        except Exception:
            return "❌ Could not determine Black Hat quality score."

        if score >= 7:
            return f"✔️ Strong Black Hat response ({score}): Proceeding."
        else:
            return f"⚠️ Weak Black Hat response ({score}): Needs revision."

    return [
        Tool(
            name="BlackHatCritiqueRater",
            func=black_hat_critique_rater,
            description="Evaluates if a response performs strong risk analysis by pointing out specific dangers and naming the type of risk.",
        )
    ]
