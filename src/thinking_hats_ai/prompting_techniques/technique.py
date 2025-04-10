from enum import Enum


class Technique(Enum):
    CHAIN_OF_THOUGHT = "chain_of_thought"
    SYSTEM_2_ATTENTION = "system_2_attention"
    CHAINING = "chaining"
    FEW_SHOT = "few_shot"
    PERSONA_PATTERN = "persona_pattern"
    CONTRASTIVE_PROMPTING = "contrastive_prompting"
    CHAIN_OF_VERIFICATION = "chain_of_verification"
    MULTI_AGENT = "multi_agent"
