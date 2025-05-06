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
    RED = "Red"
    GREEN = "Green"
    BLUE = "Blue"
    YELLOW = "Yellow"
    BLACK = "Black"


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
