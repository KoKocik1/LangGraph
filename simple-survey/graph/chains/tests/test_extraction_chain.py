from graph.chains.question_extractor import question_extractor
from graph.schema.schemas import ExtractedAnswer
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

load_dotenv()


def test_question_extractor_number() -> None:
    chat_history = []
    question = "Jaka jest Twoja waga w kg?"
    instructions = "Spróbuj wyciągnąć wagę użytkownika z odpowiedzi. Jeśli nie uda Ci się to wyciągnąć, zwróć 'None'. Waga musi być liczbą."
    human_message = "Mam 101 kg"

    answer = question_extractor.invoke(
        {
            "question_instruction": instructions,
            "question": question,
            "user_response": human_message,
            "history": []
        }
    )

    assert answer.answer == "101"


def test_question_extractor_none() -> None:
    chat_history = []
    question = "Jaka jest Twoja waga w kg?"
    instructions = "Spróbuj wyciągnąć wagę użytkownika z odpowiedzi. Jeśli nie uda Ci się to wyciągnąć, zwróć 'None'. Waga musi być liczbą."
    human_message = "Mam XAD"
    chat_history.append(human_message)

    answer = question_extractor.invoke(
        {"question_instruction": instructions,
            "question": question, "user_response": human_message, "history": []}
    )

    assert answer.answer == "None"
