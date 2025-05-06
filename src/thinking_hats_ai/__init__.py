from .brainstorming_session import BrainstormingSession
from .hats.hats import Hat
from .prompting_techniques.technique import Technique
from .utils.brainstorming_input import BrainstormingInput

"""
This module exposes the core interface for the thinking_hats_ai package.

It imports and re-exports the main components:
- BrainstormingSession: Orchestrates the full brainstorming process.
- Hat: Enum for selecting a thinking hat.
- Technique: Enum representing prompting strategies.
- BrainstormingInput: Data structure containing input for a session.
"""

__all__ = ["BrainstormingSession", "Hat", "Technique", "BrainstormingInput"]
