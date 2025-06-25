from typing import Any, Dict

from graph.chains.check_answer import GradeAnswer, answer_grader
from graph.state import GraphState
from langchain_core.messages import HumanMessage


def check_answer(state: GraphState) -> Dict[str, Any]:
    print("---CHECK ANSWER---")
    question = state["question"]
    user_response = state["user_response"]
    history = state.get("history", [])

    answer: GradeAnswer = answer_grader.invoke(
        {"question": question, "user_response": user_response, "history": history})

    state["is_valid"] = answer.binary_score
    return state
