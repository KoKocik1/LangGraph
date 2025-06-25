from dotenv import load_dotenv
from langgraph.graph import END, StateGraph
from graph.consts import CHECK_ANSWER, EXTRACT, RECAP, VALIDATE
from graph.nodes import check_answer, extract, summary
from graph.state import GraphState
from tool_executor import execute_tool_node

load_dotenv()


def has_value(state: GraphState) -> str:
    print("---EXTRACTED ANSWER IS NOT NONE---")
    if state["is_extracted"]:
        return VALIDATE
    else:
        return RECAP


def is_valid(state: GraphState) -> str:
    print("---QUESTION CONTAINS ANSWER FOR QUESTION---")
    is_valid = state["is_valid"]
    if is_valid:
        print("---ROUTE QUESTION TO EXTRACT---")
        return EXTRACT
    else:
        print("---ROUTE QUESTION TO RECAP---")
        return RECAP


workflow = StateGraph(GraphState)

workflow.add_node(CHECK_ANSWER, check_answer)
workflow.add_node(EXTRACT, extract)
workflow.add_node(VALIDATE, execute_tool_node)
workflow.add_node(RECAP, summary)

workflow.set_entry_point(CHECK_ANSWER)
workflow.add_conditional_edges(
    CHECK_ANSWER,
    is_valid,
    {
        EXTRACT: EXTRACT,
        RECAP: RECAP,
    },
)
workflow.add_conditional_edges(
    EXTRACT,
    has_value,
    {
        VALIDATE: VALIDATE,
        RECAP: RECAP,
    },
)
workflow.add_edge(VALIDATE, RECAP)
workflow.add_edge(RECAP, END)

app = workflow.compile()

app.get_graph().draw_mermaid_png(output_file_path="graph.png")
