from typing import Any, Dict

from graph.chains.question_extractor import question_extractor
from graph.schema.schemas import ExtractedAnswer
from graph.state import GraphState
from langchain_core.messages import HumanMessage


def extract(state: GraphState) -> Dict[str, Any]:
    print("---EXTRACT---")
    question = state["question"]
    instructions = state["instructions"]
    user_response = state["user_response"]
    history = state.get("history", [])
    answer: ExtractedAnswer = question_extractor.invoke(
        {
            "question_instruction": instructions,
            "question": question,
            "user_response": user_response,
            "history": history
        })

    state["is_extracted"] = answer.extracted
    if answer.extracted:
        state["extracted_answer"] = answer.answer
    return state
