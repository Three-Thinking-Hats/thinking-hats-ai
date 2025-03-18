from typing import List


class BrainstormingInput:
    def __init__(
        self,
        question: str,
        ideas: List[str],
        response_length: str = "10 sentences",
    ):
        self.question = question
        self.ideas = ideas
        self.response_length = response_length
