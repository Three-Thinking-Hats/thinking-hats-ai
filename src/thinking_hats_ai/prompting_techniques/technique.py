from enum import Enum


class Technique(Enum):
    CHAIN_OF_THOUGHT = "chain_of_thought"
    SYSTEM_2_ATTENTION = "system_2_attention"
    CHAINING = "chaining"
    FEW_SHOT = "few_shot"
