from typing import List


def list_to_bulleted_string(lst: List[str]) -> str:
    """
    Converts a list of strings into a single bulleted string.

    Each item in the input list is prefixed with a dash and a space, and the items are joined with newline characters.

    Args:
        lst (List[str]): A list of strings to be converted.

    Returns:
        str: A single string with each list item on a new line, prefixed by a bullet point.
    """
    return "\n".join([f"- {item}" for item in lst])
