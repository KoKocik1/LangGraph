from graph.graph import app
from dotenv import load_dotenv
from tool_executor import QUESTIONS
from langchain_core.messages import HumanMessage, AIMessage
load_dotenv()


if __name__ == "__main__":
    print("Hello Simple Survey")
    history = []
    questions_iterator = iter(QUESTIONS.items())
    question, details = next(questions_iterator)
    instructions = details["instruction"]
    range = f"Range: {details['min_value']} - {details['max_value']}"

    while True:
        human_message = input(question)
        history.append(HumanMessage(content=human_message))
        res = app.invoke(
            input={
                "question": question,
                "instructions": instructions,
                "user_response": human_message,
                "history": history
            })
        summary = res["summary"]
        history.append(AIMessage(content=summary))
        print(summary)
        if "is_validated" in res and res["is_validated"]:
            try:
                question, details = next(questions_iterator)
                instructions = details["instruction"]
                range = f"Range: {details['min_value']} - {details['max_value']}"
            except StopIteration:
                print("Dziękuję za wypełnienie ankiety!")
                break
