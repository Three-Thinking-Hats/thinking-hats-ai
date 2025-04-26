from langchain.tools import Tool


def get_red_hat_tools(llm):
    def feelings_assesor(input_text: str):
        prompt = f"""
                You are a feelings assesor.
                Asses if the following contribuition to a brainstorming session if it is grounded in feeling. It shouldn't be about facts, it should be about how the contributor feels. It should be about how they feel.
                - good example: **I feel** that this idea won't work out or **I have a hunch** that in the future none of this will be relevant (emotions are allowed in the thinking process and there is no need for explanation).
                All starts like "I feel" or "I have a hunch" or "I have a bad feeling" are great! All contributions starting with "I" are great.
                The red hat should not give ideas about emotions e.g. - bad examples: the company should host emotional events or The company should forster connection. (this is not grounded in emotion but about emotion. We do not want that.)

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
            name="FeelingsAssesor",
            func=feelings_assesor,
            description="Analyzes if the contribution is grounded in feeling.",
        ),
    ]
