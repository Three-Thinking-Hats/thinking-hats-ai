from langchain.tools import Tool


def get_red_hat_tools(llm):
    def sentiment_analysis_limiter(input_text: str):
        prompt = f"""
                You are an emotional sentiment assessor.
                Analyze the **emotional sentiment** of the following idea on a scale from -10 (very negative) to 10 (very positive).
                Only return the sentiment score (a number between -10 and 10) followed by a short emotion word, nothing else.

                Text: "{input_text}"

                Format: <score> <emotion>

                Sentiment Score:
                """
        response = llm.invoke(prompt)
        result = response.content.strip()
        try:
            score_part = result.strip().split()[0]
            score = float(score_part)
        except Exception:
            return "Could not determine sentiment score."

        if score >= 7 or score <= -7:
            return f"✔️ Sentiment high enough ({score}): Proceeding with idea.\n{input_text}"
        else:
            return f"❌ Sentiment too low ({score}): This idea is blocked by Red Hat's intuition."

    def red_hat_classifier(input_text: str):
        prompt = f"""
                You are a Red Hat classifier.
                Asses if the following contribuition to a brainstorming session satisfies the instructions of the red hat.
                The red hat should not give contributions about emotions e.g. - bad examples: the company should host emotional events or The company should forster connection this is not what the red hat is about.
                But the red hat is about allowing emotions into the thinking process  - good example: I feel that this idea won't work out or I have a hunch that in the future none of this will be relevant (emotions are allowed in the thinking process and there is no need for explanation)

                Idea: "{input_text}"

                Only return "good" or "bad" followed by a brief explanation why that is the case. If its bad help them to get on the right track. Maybe they need to start over.

                """
        response = llm.invoke(prompt)
        result = response.content.strip()
        try:
            rating = result.strip().split()[0].lower()
        except Exception:
            return "Could not determine intuition score."

        if rating == "good":
            return f"✔️  ({rating}) Explanation: {result}"
        else:
            return f"❌ ({rating}) Explanation: {result}"

    return [
        Tool(
            name="SentimentLimiter",
            func=sentiment_analysis_limiter,
            description="Analyzes sentiment and only allows ideas through if emotional response is strong enough (>= 0.7)",
        ),
        Tool(
            name="RedHatClassifier",
            func=red_hat_classifier,
            description="Analyzes if it is a good red hat contribution. The classifier rejects and guides if it is not a good red hat contribuition and accepts if it is good.",
        ),
    ]
