from graph.chains.check_answer import answer_grader
from graph.schema.schemas import ExtractedAnswer
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()


def test_answer_grade_yes() -> None:
    question = "How old are you?"
    human_message = HumanMessage(content="I am 21 years old")

    answer = answer_grader.invoke(
        {
            "question": question,
            "user_response": human_message,
            "history": []
        }
    )

    assert answer.binary_score


def test_answer_grade_no() -> None:

    question = "How old are you?"
    human_message = HumanMessage(content="I am das years old")
    answer = answer_grader.invoke(
        {"question": question, "user_response": human_message, "history": []}
    )

    assert not answer.binary_score
