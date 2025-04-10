import io
import json
from contextlib import redirect_stdout

from autogen import ConversableAgent, GroupChat, GroupChatManager, LLMConfig
from langchain.prompts import PromptTemplate

from thinking_hats_ai.prompting_techniques.base_technique import (
    BasePromptingTechnique,
)

from ..utils.api_handler import APIHandler
from ..utils.brainstorming_input import BrainstormingInput
from ..utils.string_utils import list_to_bulleted_string


class MultiAgent(BasePromptingTechnique):
    ### Meta Prompt for Persona Generation
    def execute_prompt(
        self,
        brainstorming_input: BrainstormingInput,
        hat_instructions: str,
        api_handler: APIHandler,
    ):
        brainstorming_input.question
        template = PromptTemplate(
            input_variables=[
                "hat_instructions"
            ],
            template= "The task for a multi agent prompt is, to create a contribution to a brainstorming from the point of view of the following persona: {hat_instructions}\n"
            "They will receive a brainstorming question and a list of previously generated ideas, along to the task to create a contribution\n"
            "Your task is, to create personas as for the multi agent. There must be at least 3 personas, which are all different from each other.\n"
            "Make sure that at least one of the personas suits the description of the persona, and leads the conversation into this direction.\n"
            "Return the a json it should include a name (no whitespaces allowed) and a system_message for each persona'\n"
            "The json should be a list of dictionaries, but this list should not be a dictionary itself!"
            "Do ONLY return a valid json!"
            "Do not use ```json or ``` just return a list of dictionaries\n"
        )

        prompt = template.format(
            hat_instructions=hat_instructions,
        )

        self.logger.log_prompt(prompt, notes="META PROMPT - GENERATE PERSONAS")

        response = api_handler.get_response(prompt)

        self.logger.log_response(response, notes="META PROMPT - GENERATED PERSONAS")

        ### Prompt for Multi Agent
        llm_config = LLMConfig(api_type="openai", model="gpt-4o", api_key=api_handler.api_key)
        # 1. Format response
        if isinstance(response, str):
            response = json.loads(response)
        # 2. Create the agents
        agents = []
        with llm_config:
            for persona in response:
                agent = ConversableAgent(
                    persona["name"],
                    system_message=(persona["system_message"] + "\n If you found a contribution meeting the initial critera respond ONLY with 'FINAL: (CONTRIBUTION)', do not add quotation marks or any other content, do not make a final contribution while still saying anything else. Make sure everyone at least contributed three times before you allign.")
                )
                agents.append(agent)

        # 3. Create groupchat
        groupchat = GroupChat(
            agents=agents,
            speaker_selection_method="auto",
            max_round=30
        )
        # 4. Create manager
        manager = GroupChatManager(
            name="group_manager",
            groupchat=groupchat,
            system_message="you are the leader of the discussion. You want to assure that the agents do not allign to quickly (not before everyone contributed at least twice). You ensure that the task will be fullfilled.",
            llm_config=llm_config,
            is_termination_msg=lambda x: "FINAL:" in (x.get("content", "") or "").upper(),
        )
        # 5. Run the chat
        response = manager.run(
            recipient=manager,
            message="Let's find a contribution to the brainstorming question: {question}" \
                "Our goal is to create a contribution to the brainstorming from the point of view of the following persona: {hat_instructions}\n" \
                "These are the currently developed ideas in the brainstorming:\n{ideas}\n" \
                "Discuss what you could contribute to the brainstorming while sticking to the defined persona. Your goal is to either create a new contribution or use the existing ones. It may depend on the persona defined above.\n" \
                "The discussion should take at least 19 turns, and each persona should contribute at least three times. While discussing the length isn't important, only for the final contribution.\n" \
                "The final contribution should be {length} long and fullfill the previous criteria.".format(
                question=brainstorming_input.question,
                ideas=list_to_bulleted_string(brainstorming_input.ideas),
                hat_instructions=hat_instructions,
                length=brainstorming_input.response_length
            )
        )
        # 6. Iterate through the chat automatically with & without console output
        if not self.logger.dev:
            with redirect_stdout(io.StringIO()):
                response.process()
        else:
            response.process()

        # 6.1 Collect the full conversation transcript
        chat_transcript = ""
        for msg in groupchat.messages:
            name = msg.get("name", "Unknown")
            content = msg.get("content", "")
            contrib = f"{name}: {content}\n"
            chat_transcript += contrib
            self.logger.log_response_and_prompt(contrib, notes="CHAT CONTRIBUTION")

        # log if found final
        lastMessage = groupchat.messages[-1].get("content","")
        if lastMessage.startswith("FINAL:"):
            final = lastMessage.replace("FINAL: ", "", 1)
            return final

        # 6.2 If no final contribution found yet, create one
        final_prompt = (
            f"Here is the transcript of a brainstorming discussion among multiple personas:\n\n"
            f"{chat_transcript}\n\n"
            f"Based on this discussion, provide ONE clear, concise final contribution to the brainstorming question:\n"
            f"'{brainstorming_input.question}'\n\n"
            f"The contribution should reflect the collective insights and be approximately {brainstorming_input.response_length} long.\n"
            f"Only return the final contribution—no introduction, no extra commentary. Do not put your response in quotation marks."
        )

        self.logger.log_prompt(final_prompt, notes="FINAL CONTRIBUTION PROMPT")
        final_response = api_handler.get_response(final_prompt)
        self.logger.log_response(final_response, notes="FINAL CONTRIBUTION RESPONSE")

        return final_response


