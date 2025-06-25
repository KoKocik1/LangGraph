from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableSequence
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import datetime
from typing import List, Union

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from graph.schema.schemas import ExtractedAnswer, OutputAnswer

load_dotenv()

llm = ChatOpenAI(model="o4-mini")
structured_llm_grader = llm.with_structured_output(ExtractedAnswer)
parser_pydantic = PydanticToolsParser(tools=[ExtractedAnswer])

system = """Jesteś eksperciem w wyciąganiu informacji z odpowiedzi użytkownika.
Aktualny czas: {time}

1. Pytanie: {question}
2. Instrukcje: {question_instruction}
3. Spróbuj zrozumieć odpowiedź użytkownika i wyciągnij z niej informacje.
4. Wyciągnij informacje z odpowiedzi użytkownika w wymaganym formacie.
5. Odpowiedz moze byc w formie zdania, pytania lub odpowiedzi. Jezeli odpowiedz jest zdaniem to wyciagnij z niego informacje.
6. Jeśli nie znajdziesz informacji, zwróć 'None'.
"""

# === Prompt template ===
question_extractor_prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{user_response}")
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),
)


# question_extractor = question_extractor_prompt_template | llm | StrOutputParser()
question_extractor = question_extractor_prompt_template | structured_llm_grader
