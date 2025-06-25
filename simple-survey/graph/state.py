from typing import List, TypedDict
from langchain_core.messages import BaseMessage


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        question: general question
        instructions: instructions for processing answer
        user_response: user response
        extracted_answer: answer to question
        history: conversation history

        is_valid: contains answer for question # 1 step
        is_extracted: extracted answer from question # 2 step
        is_validated: validated answer from question # 3 step
        saved: saved answer to database # 4 step
        summary: summary of answer # 5 step
    """

    question: str
    instructions: str
    user_response: str
    extracted_answer: str
    range: str
    history: List[BaseMessage]

    is_valid: bool
    is_extracted: bool
    is_validated: bool
    summary: str
