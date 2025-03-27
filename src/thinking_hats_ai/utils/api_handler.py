from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI


class APIHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.chat_model = ChatOpenAI(
            model_name="gpt-4o", openai_api_key=self.api_key
        )

    def get_response(self, prompt):
        response = self.chat_model.invoke([HumanMessage(content=prompt)])
        return response.content
