from typing import List


def list_to_bulleted_string(lst: List[str]) -> str:
    return "\n".join([f"- {item}" for item in lst])
