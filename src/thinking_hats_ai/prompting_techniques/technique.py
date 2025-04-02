from enum import Enum


class Technique(Enum):
    CHAIN_OF_THOUGHT = "chain_of_thought"
    PERSONA_PATTERN = "persona_pattern"
    CONTRASTIVE_PROMPTING = "contrastive_prompting"
    CHAIN_OF_VERIFICATION = "chain_of_verification"
