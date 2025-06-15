from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
load_dotenv()


@tool
def triple(num: float) -> float:
    """
    Param num: The float number to triple.
    Returns: The float number tripled.
    """
    return num * 3


tools = [TavilySearch(max_results=1), triple]

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0).bind_tools(tools)
