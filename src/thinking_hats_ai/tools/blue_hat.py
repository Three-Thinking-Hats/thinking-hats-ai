from langchain.tools import Tool


def get_blue_hat_tools(llm):
    def thinking_process_manager_rater(input_text: str):
        prompt = f"""
            You are an evaluator of thinking process management quality.
            Analyze the following statement and rate how well it demonstrates control over the thinking process.

            Thinking process management includes:
            - Setting or clarifying goals
            - Planning next thinking steps
            - Coordinating different thinking styles (e.g. facts, emotions, critique)
            - Summarizing progress or directing attention
            - Keeping the brainstorming session structured and focused

            Rate the statement on a scale from 0 (not managing thinking at all) to 10 (very clearly managing the thinking process).
            Be strict and fair.

            Text: "{input_text}"

            Only return the score followed by one or two words explaining why.

            Format: <score> <reason>

            Process Management Score:
            """
        response = llm.invoke(prompt)
        result = response.content.strip()
        print(f"Raw LLM response: {result}")
        try:
            score_part = result.strip().split()[0]
            score = float(score_part)
        except Exception:
            return "Could not determine process management score."

        if score >= 7:
            return f"🟦 Strong thinking process management ({score}): Proceeding.\n{input_text}"
        else:
            return f"⚠️ Process management too weak ({score}): Not accepted by Blue Hat standards."

    return [
        Tool(
            name="ThinkingProcessRater",
            func=thinking_process_manager_rater,
            description="Rates a statement from 0–10 for its ability to manage the thinking process (e.g., goal setting, agenda planning, coordination).",
        )
    ]
