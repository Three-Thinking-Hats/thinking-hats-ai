from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

class APIHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.chat_model = ChatOpenAI(model_name="gpt-4o", openai_api_key=self.api_key)

    def get_response(self, prompt):
        response = self.chat_model([HumanMessage(content=prompt)])
        return response.content
