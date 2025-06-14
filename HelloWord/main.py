from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import MessagesState, StateGraph, END
from nodes import run_agent_reasoning, tool_node
load_dotenv()

AGENT_REASON = "agent_reason"
ACT = "act"
LAST = -1


def should_continue(state: MessagesState) -> str:
    """
    Check if the last messsage is a tool call.
    """
    if not state["messages"][LAST].tool_calls:
        return END
    return ACT


graph = StateGraph(MessagesState)

# Add nodes
graph.add_node(AGENT_REASON, run_agent_reasoning)
graph.add_node(ACT, tool_node)

# Set entry point
graph.set_entry_point(AGENT_REASON)

# Add conditional edges
graph.add_conditional_edges(AGENT_REASON, should_continue, {
    END: END,
    ACT: ACT
})

# Add edge from ACT to AGENT_REASON
graph.add_edge(ACT, AGENT_REASON)

# Compile the graph
app = graph.compile()

# Generate graph visualization
app.get_graph().draw_mermaid_png(output_file_path="graph.png")


if __name__ == "__main__":
    content = "What is the temperature in Tokyo? List it and then triple it"
    messages = {"messages": [HumanMessage(content=content)]}
    res = app.invoke(messages)
    print(res["messages"][LAST].content)
