from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage

llm = ChatOpenAI(temperature=0)
summary_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Jestes eksperciem w tworzeniu podsumowań.

Instrukcje: 
1. Możesz zwrócić informację o nieprawidłowej walidacji.
2. Możesz zwrócić informację o zapisaniu odpowiedzi. Dodaj informację o zapisanej wartości.
3. Możesz zwrócić informacje istotne dla pytania użytkownika w obszarze pytania.
4. IMPORTANT: próbuj mówić do użytkownika w sposób przyjazny, jakby był człowiekiem. Zawsze zwracaj zdanie lub dwa.
5. IMPORTANT: Zawsze zwracaj podsumowanie w przynajmniej jednym zdaniu. Nie zwracaj pojedynczych slow. Uzytkownik musi zrozumiec komunikat.

""",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{user_response}"),
        ("system", "Odpowiedz wymaganym formatem."),
    ]
)

generation_chain = summary_prompt_template | llm | StrOutputParser()


if __name__ == "__main__":
    print(generation_chain.invoke(
        {"messages": [
            SystemMessage(content="You are expert summary agent."),
            HumanMessage(content="Jaka jest Twoja waga w kg?")]}))
