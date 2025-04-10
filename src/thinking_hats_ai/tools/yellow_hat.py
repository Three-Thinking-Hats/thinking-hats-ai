from langchain.tools import Tool


def get_yellow_hat_tools(llm):
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
        print(f"Raw LLM response: {result}")
        try:
            score_part = result.strip().split()[0]
            score = float(score_part)
        except Exception:
            return "Could not determine sentiment score."

        if score >= 7:
            return f"✔️ Sentiment positive enough ({score}): Proceeding with idea.\n{input_text}"
        else:
            return f"❌ Sentiment too negative ({score}): This idea is blocked by Yellow Hat's intuition."

    return [
        Tool(
            name="SentimentLimiter",
            func=sentiment_analysis_limiter,
            description="Analyzes sentiment and only allows ideas through if emotional response is strong enough (>= 0.7)",
        )
    ]
