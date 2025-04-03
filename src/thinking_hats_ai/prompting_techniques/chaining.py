from langchain.prompts import PromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory

from thinking_hats_ai.prompting_techniques.base_technique import BasePromptingTechnique

from ..utils.api_handler import APIHandler
from ..utils.brainstorming_input import BrainstormingInput
from ..utils.string_utils import list_to_bulleted_string


class Chaining(BasePromptingTechnique):
    def execute_prompt(
        self,
        brainstorming_input: BrainstormingInput,
        hat_instructions: str,
        api_handler: APIHandler,
    ):
        chat_history = ChatMessageHistory()

        initial_prompt_template = PromptTemplate(
            input_variables=["hat_instructions"],
            template="Imagine you are wearing the following thinking hat: {hat_instructions}",
        )

        chain1 = initial_prompt_template | api_handler.chat_model

        formatted_prompt = initial_prompt_template.format(hat_instructions=hat_instructions)
        chat_history.add_user_message(formatted_prompt)
        self.logger.log_prompt(formatted_prompt)

        hat_output = chain1.invoke(input={"hat_instructions": hat_instructions})
        chat_history.add_ai_message(hat_output.content)

        # Chain Part 2: Generate Ideas

        formatted_history = "\n".join(
            [f"{msg.type.upper()}: {msg.content}" for msg in chat_history.messages]
        )

        refinement_prompt_template = PromptTemplate(
            input_variables=["chat_history", "question", "ideas"],
            template=(
                "Chat history so far:\n{chat_history}\n"
                "This is the question that was asked in the brainstorming: {question}\n"
                "These are the ideas that are currently in the brainstorming:\n{ideas}\n"
                "Contribute to the brainstorming from the perspective of the thinking hat.\n"
            ),
        )

        chain2 = refinement_prompt_template | api_handler.chat_model

        question_val = brainstorming_input.question
        ideas_val = list_to_bulleted_string(brainstorming_input.ideas)

        refined_output = chain2.invoke(
            input={
                "chat_history": formatted_history,
                "hat_instructions": hat_instructions,
                "question": question_val,
                "ideas": ideas_val,
            }
        )
        chat_history.add_ai_message(refined_output.content)

        # Chain Part 3: Refinement

        formatted_history = "\n".join(
            [f"{msg.type.upper()}: {msg.content}" for msg in chat_history.messages]
        )

        final_prompt_template = PromptTemplate(
            input_variables=["chat_history", "length"],
            template=(
                "Chat history so far:\n{chat_history}\n"
                "Review the conversation and refine the outcome further to ensure it fully aligns with the thinking hat's perspective:\n"
                "Provide a final, polished answer with a length of {length}.\n"
            ),
        )
        chain3 = final_prompt_template | api_handler.chat_model

        length_val = brainstorming_input.response_length
        final_idea = chain3.invoke(
            input={
                "chat_history": formatted_history,
                "refined_output": refined_output.content,
                "length": length_val,
            }
        )
        chat_history.add_ai_message(final_idea.content)

        # print(f"Hat Output: {hat_output.content}")
        # print(f"Refined Output: {refined_output.content}")
        # print(f"Final Idea: {final_idea.content}")

        return final_idea.content
