from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class GradeAnswer(BaseModel):

    binary_score: bool = Field(
        description="True jeżeli odpowiedź zawiera informację zapytania, nawet jeśli jest zawarta w zdaniu. False w przeciwnym wypadku."
    )


llm = ChatOpenAI(temperature=0)
structured_llm_grader = llm.with_structured_output(GradeAnswer)

system = """Jesteś eksperciem w ocenianiu, czy odpowiedź zawiera informację zapytania.

Zwróć binarną ocenę: True lub False.

- True oznacza, że odpowiedź użytkownika zawiera informację zapytania, nawet jeśli jest zawarta w zdaniu.
- False oznacza, że użytkownik nie podał odpowiedzi (np. uniknął, zmienił temat lub był niejasny).

Uzytkownik moze podac odpowiedz w formie zdania, pytania lub odpowiedzi.
Sprawdz czy odpowiedz jest odpowiedzią na pytanie. Musisz byc 100% pewny ze odpowiedz jest odpowiedzią na pytanie.
Jezeli masz wątpliwości, zwróć False.

IMPORTANT: Jezeli nie znalazles informacji w odpowiedzi, zwróć False.

Przykłady:

Pytanie: Ile masz lat?
Odpowiedź użytkownika: Mam 21 lat → True

Pytanie: Jak się masz na imię?
Odpowiedź użytkownika: Mam na imię Alice → True

Pytanie: Ile masz lat?
Odpowiedź użytkownika: Nie chcę Ci powiedzieć → False

Pytanie: Ile masz lat?
Odpowiedź użytkownika: Lubię pizzę → False
"""
answer_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        MessagesPlaceholder(variable_name="history"),
        ("human",
         "Pytanie: {question} \n\n Odpowiedź użytkownika: {user_response}"),
    ]
)

answer_grader: RunnableSequence = answer_prompt | structured_llm_grader
