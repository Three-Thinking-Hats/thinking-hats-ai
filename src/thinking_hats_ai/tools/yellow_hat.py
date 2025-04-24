from langchain.tools import Tool


def get_yellow_hat_tools(llm):
    def yellow_hat_value_assessor(input_text: str):
        prompt = f"""
        You are a Yellow Hat assessor. Evaluate whether the following response demonstrates **positive, opportunity-focused thinking** as expected from the Yellow Hat role in a brainstorming session.

        A proper Yellow Hat response should:
        - Highlight **potential benefits** or **positive outcomes**
        - Name specific **stakeholders** who benefit (e.g., students, faculty, partners)
        - Point out **opportunities for growth, impact, or efficiency**
        - Identify **value gaps** (what could be improved to deliver more value)
        - Suggest a direction to **enhance these benefits** — either by building on an existing idea or proposing a new one

        It should not be vague praise or general enthusiasm. It must demonstrate constructive value-focused thinking.

        Rate the response from 0 (not Yellow Hat at all) to 10 (excellent Yellow Hat thinking).

        Response to evaluate:
        \"\"\"{input_text}\"\"\"

        Only return the score followed by a short reason.

        Format: <score> <reason>

        Yellow Hat Score:
        """
        response = llm.invoke(prompt)
        result = response.content.strip()
        print(f"Raw LLM response: {result}")
        try:
            score_part = result.strip().split()[0]
            score = float(score_part)
        except Exception:
            return "❌ Could not determine Yellow Hat score."

        if score >= 7:
            return f"🟨 Strong Yellow Hat response ({score}): Proceeding."
        else:
            return f"⚠️ Weak Yellow Hat response ({score}): Needs revision."

    return [
        Tool(
            name="YellowHatValueRater",
            func=yellow_hat_value_assessor,
            description="Evaluates whether a response highlights specific benefits, value opportunities, or positive impacts as expected from the Yellow Hat.",
        )
    ]
