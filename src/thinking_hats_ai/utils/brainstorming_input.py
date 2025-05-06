from typing import List


class BrainstormingInput:
    """
    A data container for storing input to a brainstorming process.

    This class holds a main question, a list of ideas related to that question, and an optional expected response length.
    """

    def __init__(
        self,
        question: str,
        ideas: List[str],
        response_length: str = "10 sentences",
    ):
        """
        Initializes a BrainstormingInput instance.

        Args:
            question (str): The main question to be brainstormed.
            ideas (List[str]): A list of supporting ideas or thoughts related to the question.
            response_length (str, optional): Suggested length of the response (e.g., '10 sentences'). Defaults to "10 sentences".
        """
        self.question = question
        self.ideas = ideas
        self.response_length = response_length
