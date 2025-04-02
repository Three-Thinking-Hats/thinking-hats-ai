from enum import Enum


class Technique(Enum):
    CHAIN_OF_THOUGHT = "chain_of_thought"
    ZERO_SHOT_COT = "zero_shot_cot"
    EMOTION_PROMPT = "emotion_prompt"
    REACT = "re_act"
    TAKE_A_STEP_BACK = "take_a_step_back"
