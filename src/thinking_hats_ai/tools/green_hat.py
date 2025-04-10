from langchain.tools import Tool


def get_green_hat_tools(llm):
    def creativity_scorer(input_text: str):
        prompt = f"""
            You are a creativity evaluator.
            Analyze the creativity of the following idea on a scale from 0 (not creative at all) to 10 (extremely creative).
            Base your rating on originality, unexpectedness, and novelty. Do not consider usefulness or practicality.
            Be hard.

            Text: "{input_text}"

            Only return the creativity score followed by one or two words explaining why.

            Format: <score> <reason>

            Creativity Score:
            """
        response = llm.invoke(prompt)
        result = response.content.strip()
        print(f"Raw LLM response: {result}")
        try:
            score_part = result.strip().split()[0]
            score = float(score_part)
        except Exception:
            return "Could not determine creativity score."

        if score >= 7:
            return f"🟢 High creativity ({score}): Proceeding with idea.\n{input_text}"
        else:
            return f"🔴 Creativity too low ({score}): This idea is blocked by Green Hat's standards."

    return [
        Tool(
            name="CreativityScorer",
            func=creativity_scorer,
            description="Evaluates the creativity of an idea (0–10) and blocks ideas below 7 on the creativity scale.",
        )
    ]
