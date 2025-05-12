from enum import Enum

from thinking_hats_ai.hats.black import BlackHat
from thinking_hats_ai.hats.blue import BlueHat
from thinking_hats_ai.hats.green import GreenHat
from thinking_hats_ai.hats.red import RedHat
from thinking_hats_ai.hats.white import WhiteHat
from thinking_hats_ai.hats.yellow import YellowHat


class Hat(Enum):
    """
    Enum representing the six distinct thinking hats from Edward de Bono's method.

    Each hat corresponds to a specific thinking style used during structured brainstorming.
    """

    WHITE = "White"
    """
    Represents the White Hat thinking role, focused on facts, evidence, and neutrality.

    This hat emphasizes analyzing existing ideas by identifying known facts,
    highlighting knowledge gaps, and ensuring that reasoning is based on data and logic.
    """

    RED = "Red"
    """
    Represents the Red Hat thinking role, which focuses on expressing emotional responses, intuition, and gut feelings.

    This hat encourages subjective reactions to existing ideas in the brainstorming session,
    without requiring logical justification. Its purpose is to surface the emotional tone of the discussion.
    """

    GREEN = "Green"
    """
    Represents the Green Hat thinking role, which focuses on creativity, innovation, and new possibilities.

    This hat encourages original thinking, alternative suggestions, and provocative or unconventional ideas.
    It is used to expand and enrich the brainstorming process through imaginative contributions.
    """

    BLUE = "Blue"
    """
    Represents the Blue Hat thinking role, which focuses on facilitating, directing, and maintaining
    the structure and quality of the brainstorming process.

    This hat does not contribute new content but guides the discussion by evaluating which thinking style
    (e.g., creative, cautious, factual) is most appropriate, and by helping the group stay on topic,
    clarify ideas, or further develop underexplored contributions.
    """

    YELLOW = "Yellow"
    """
    Represents the Yellow Hat thinking role, focused on identifying benefits,
    opportunities, and value in existing brainstorming ideas.
    """

    BLACK = "Black"
    """
    Represents the Black Hat thinking role, which focuses on critical judgment and risk assessment.

    This hat is responsible for identifying weaknesses, potential pitfalls, and unintended consequences
    in existing brainstorming ideas. It promotes caution and helps refine ideas by pointing out flaws or threats.
    """


class Hats:
    """
    Provides access to the instructional content for each thinking hat.

    This class acts as a bridge between the `Hat` enum and the corresponding instructional
    text defined in each individual hat module.
    """

    INSTRUCTIONS = {
        Hat.WHITE: WhiteHat.INSTRUCTION,
        Hat.RED: RedHat.INSTRUCTION,
        Hat.GREEN: GreenHat.INSTRUCTION,
        Hat.BLUE: BlueHat.INSTRUCTION,
        Hat.YELLOW: YellowHat.INSTRUCTION,
        Hat.BLACK: BlackHat.INSTRUCTION,
    }

    def get_instructions(self, hat):
        """
        Retrieves the instruction string associated with a given thinking hat.

        Args:
            hat (Hat): The thinking hat enum value.

        Returns:
            str: Instruction text for the selected hat, or a fallback message if not found.
        """
        return self.INSTRUCTIONS.get(hat, "Invalid hat specified.")
