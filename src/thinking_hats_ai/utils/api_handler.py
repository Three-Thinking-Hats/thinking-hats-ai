from langchain.schema import HumanMessage
from langchain_openai import ChatOpenAI


class APIHandler:
    """
    A simple handler for interacting with the OpenAI Chat API using a specified model.

    Provides functionality to send prompts and switch models dynamically.
    """

    def __init__(self, api_key, model="gpt-4.1"):
        """
        Initializes the APIHandler with an API key and model.

        Args:
            api_key (str): The OpenAI API key.
            model (str, optional): The model to use for chat (default is "gpt-4.1").
        """
        self.api_key = api_key
        self.chat_model = ChatOpenAI(
            model_name=model, openai_api_key=self.api_key
        )

    def get_response(self, prompt):
        """
        Sends a prompt to the model and retrieves the response.

        Args:
            prompt (str): The prompt to send to the model.

        Returns:
            str: The content of the model's response.
        """
        response = self.chat_model.invoke([HumanMessage(content=prompt)])
        return response.content

    def change_model(self, model):
        """
        Changes the model used by the API handler.

        Args:
            model (str): The new model name to use.
        """
        self.chat_model = ChatOpenAI(
            model_name=model, openai_api_key=self.api_key
        )
