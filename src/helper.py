from typing import Literal
from collections.abc import Mapping

STREAMLIT_ROLE = Literal["user", "assistant"]

class StreamlitMessage:
    def __init__(self, content: str | Mapping, role: STREAMLIT_ROLE):
        self.content = content
        self.role = role