from langchain.prompts import PromptTemplate

from thinking_hats_ai.prompting_techniques.base_technique import (
    BasePromptingTechnique,
)


class ChainOfThought(BasePromptingTechnique):
    def generate_prompt(self, input_text, hat_instructions):
        template = PromptTemplate(
            input_variables=["hat_instructions", "input_text"],
            template="Imagine you wear a hat with the following instructions: {hat_instructions}\\n\\n"
            "This is the current state of the brainstorming: {input_text}"
            "What would you add from the perspective of the given hat? Justify your answer and give reasoning about you thought process step-by-step:\\n",
        )
        return template.format(
            hat_instructions=hat_instructions, input_text=input_text
        )
