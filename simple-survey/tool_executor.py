from dotenv import load_dotenv
from typing import Union
from langchain_core.tools import StructuredTool, tool
from langgraph.prebuilt import ToolNode
from graph.state import GraphState
from datetime import datetime

load_dotenv()

QUESTIONS = {
    "Ile masz lat?": {
        "instruction": "Spróbuj wyciągnąć wiek z odpowiedzi użytkownika. Wiek musi być liczbą.",
        "min_value": 10,
        "max_value": 120
    },
    "Jaki jest twój rok urodzenia?": {
        "instruction": "Spróbuj wyciągnąć rok urodzenia z odpowiedzi użytkownika. Rok urodzenia musi być liczbą 4 cyfrową.",
        "min_value": datetime.now().year - 120,
        "max_value": datetime.now().year
    }
}


def validate_range(value: Union[int, float], min_value: Union[int, float], max_value: Union[int, float]) -> bool:
    """Sprawdza czy wartość mieści się w określonym zakresie."""
    return min_value <= value <= max_value


def validate_answer(extracted_answer: str, question_data: dict) -> bool:
    """Sprawdza czy odpowiedź jest poprawna."""
    if not question_data:
        return True  # nothing to validate
    if validate_range(float(extracted_answer), question_data["min_value"], question_data["max_value"]):
        return True
    return False


def execute_tool_node(state: GraphState) -> GraphState:
    print("---VALIDATE ANSWER---")
    question_data = QUESTIONS.get(state["question"])
    result = validate_answer(
        extracted_answer=state["extracted_answer"],
        question_data=question_data,
    )
    state["is_validated"] = result
    state["range"] = f"Zakres: {question_data['min_value']} - {question_data['max_value']}"
    return state
