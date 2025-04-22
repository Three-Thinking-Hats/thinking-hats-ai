from langchain.tools import Tool


def get_red_hat_tools(llm):
    def red_hat_classifier(input_text: str):
        prompt = f"""
                You are a Red Hat classifier.
                Asses if the following contribuition to a brainstorming session satisfies the instructions of the red hat.
                The red hat should not give contributions about emotions e.g. - bad examples: the company should host emotional events or The company should forster connection this is not what the red hat is about. There should be no ideas connected to emotion just because it is the red hat.
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
            name="RedHatClassifier",
            func=red_hat_classifier,
            description="Analyzes if it is a good red hat contribution. The classifier rejects and guides if it is not a good red hat contribuition and accepts if it is good.",
        ),
    ]
