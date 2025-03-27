from enum import Enum

from thinking_hats_ai.hats.black import BlackHat
from thinking_hats_ai.hats.blue import BlueHat
from thinking_hats_ai.hats.green import GreenHat
from thinking_hats_ai.hats.red import RedHat
from thinking_hats_ai.hats.white import WhiteHat
from thinking_hats_ai.hats.yellow import YellowHat


class Hat(Enum):
    WHITE = "White"
    RED = "Red"
    GREEN = "Green"
    BLUE = "Blue"
    YELLOW = "Yellow"
    BLACK = "Black"


class Hats:
    INSTRUCTIONS = {
        Hat.WHITE: WhiteHat.INSTRUCTION,
        Hat.RED: RedHat.INSTRUCTION,
        Hat.GREEN: GreenHat.INSTRUCTION,
        Hat.BLUE: BlueHat.INSTRUCTION,
        Hat.YELLOW: YellowHat.INSTRUCTION,
        Hat.BLACK: BlackHat.INSTRUCTION,
    }

    def get_instructions(self, hat):
        return self.INSTRUCTIONS.get(hat, "Invalid hat specified.")
