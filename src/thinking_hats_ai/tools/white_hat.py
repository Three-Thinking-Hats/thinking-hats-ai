from langchain.tools import Tool


def get_white_hat_tools(llm):
    def sentiment_analysis_limiter(input_text: str):
        prompt = f"""
                You are an neutral sentiment assessor.
                Analyze the neutrality of the following idea on a scale from -10 (very emotional in the negative sense) to 10 (very emotional in the positive sense) where 0 would be neutral.
                Only return the sentiment score (a number between -10 and 10) followed by a short emotion word if possible, nothing else.

                Text: "{input_text}"

                Format: <score> <emotion>

                Sentiment Score:
                """
        response = llm.invoke(prompt)
        result = response.content.strip()
        print(f"Raw LLM response: {result}")
        try:
            score_part = result.strip().split()[0]
            score = float(score_part)
        except Exception:
            return "Could not determine sentiment score."

        if score <= 4 and score >= -4:
            return f"✔️ Sentiment low enough ({score}): Proceeding with idea.\n{input_text}"
        else:
            return f"❌ Sentiment too high ({score}): This idea is blocked."

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
    # Tool(
    #     name="SentimentLimiter",
    #     func=sentiment_analysis_limiter,
    #     description="Analyzes sentiment and only allows ideas through if emotional response is strong enough (>= 0.7)",
    # )
