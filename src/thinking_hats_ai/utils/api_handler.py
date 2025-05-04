from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI


class APIHandler:
    def __init__(self, api_key, model="gpt-4.1"):
        self.api_key = api_key
        self.chat_model = ChatOpenAI(
            model_name=model, openai_api_key=self.api_key
        )

    def get_response(self, prompt):
        response = self.chat_model.invoke([HumanMessage(content=prompt)])
        return response.content

    def change_model(self, model):
        self.chat_model = ChatOpenAI(
            model_name=model, openai_api_key=self.api_key
        )
