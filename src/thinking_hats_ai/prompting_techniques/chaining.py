from langchain.prompts import PromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory

from thinking_hats_ai.hats.hats import Hat, Hats
from thinking_hats_ai.prompting_techniques.base_technique import (
    BasePromptingTechnique,
)

from ..utils.api_handler import APIHandler
from ..utils.brainstorming_input import BrainstormingInput
from ..utils.string_utils import list_to_bulleted_string


class Chaining(BasePromptingTechnique):
    def execute_prompt(
        self,
        brainstorming_input: BrainstormingInput,
        hat: Hat,
        api_handler: APIHandler,
    ):
        self.api_handler = api_handler
        chat_history = ChatMessageHistory()
        self.logger.start_logger(hat.value)
        hat_instructions = Hats().get_instructions(hat)

        # Chain 1: Initial Response
        initial_prompt_template = PromptTemplate(
            input_variables=["hat_instructions"],
            template=(
                "Imagine you are wearing a thinking hat with the following instructions: {hat_instructions}\n"
                "Make sure that you correctly understand the instructions and follow them in your next responses."
            ),
        )

        self._invoke_chain(
            prompt_template=initial_prompt_template,
            formatting_data={"hat_instructions": hat_instructions},
            invocation_data={"hat_instructions": hat_instructions},
            chat_history=chat_history,
            prompt_notes="Initial Prompt",
            response_notes="Initial Response",
        )

        # Chain 2: Generate Ideas
        formatted_history = self._format_chat_history(chat_history)

        refinement_prompt_template = PromptTemplate(
            input_variables=["chat_history", "question", "ideas"],
            template=(
                "Chat history so far: {chat_history}\n"
                "This is the question that was asked in the brainstorming: {question}\n"
                "These are the ideas that are currently in the brainstorming:\n{ideas}\n"
                "Contribute to the brainstorming from the perspective of the thinking hat."
            ),
        )

        self._invoke_chain(
            prompt_template=refinement_prompt_template,
            formatting_data={
                "chat_history": "See the chat history above.",
                "question": brainstorming_input.question,
                "ideas": list_to_bulleted_string(brainstorming_input.ideas),
            },
            invocation_data={
                "chat_history": formatted_history,
                "question": brainstorming_input.question,
                "ideas": list_to_bulleted_string(brainstorming_input.ideas),
            },
            chat_history=chat_history,
            prompt_notes="Refinement Prompt",
            response_notes="Generate Ideas Response",
        )

        # Chain 3: Final Refinement
        formatted_history = self._format_chat_history(chat_history)
        final_prompt_template = PromptTemplate(
            input_variables=["chat_history", "length"],
            template=(
                "Chat history so far: {chat_history}\n"
                "Review the conversation and refine the outcome further to ensure it fully aligns with the thinking hat's perspective:\n"
                "Provide a final, polished answer with a length of {length}."
            ),
        )

        final_output = self._invoke_chain(
            prompt_template=final_prompt_template,
            formatting_data={
                "chat_history": "See the chat history above.",
                "length": brainstorming_input.response_length,
            },
            invocation_data={
                "chat_history": formatted_history,
                "length": brainstorming_input.response_length,
            },
            chat_history=chat_history,
            prompt_notes="Final Prompt",
            response_notes="Final Response",
        )

        return final_output

    def _format_chat_history(self, chat_history: ChatMessageHistory):
        return "\n" + "\n\n".join(
            f"{msg.type.upper()}: {msg.content}"
            for msg in chat_history.messages
        )

    def _log_user_message(
        self, chat_history: ChatMessageHistory, message: str, notes: str
    ):
        chat_history.add_user_message(message)
        self.logger.log_prompt(message, notes)

    def _log_ai_message(
        self, chat_history: ChatMessageHistory, message: str, notes: str
    ):
        chat_history.add_ai_message(message)
        self.logger.log_response(message, notes)

    def _invoke_chain(
        self,
        prompt_template: PromptTemplate,
        formatting_data: dict,
        invocation_data: dict,
        chat_history: ChatMessageHistory,
        prompt_notes: str,
        response_notes: str,
    ):
        formatted_prompt = prompt_template.format(**formatting_data)
        self._log_user_message(chat_history, formatted_prompt, prompt_notes)

        chain = prompt_template | self.api_handler.chat_model
        output = chain.invoke(input=invocation_data)

        self._log_ai_message(chat_history, output.content, response_notes)
        return output.content
