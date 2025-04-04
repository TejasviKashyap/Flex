import streamlit as st
from langchain_core.tools import tool
import re

# Tool definitions
@tool(return_direct=True)
def wiki_search(query: str) -> str:
    """
    Search Wikipedia for the given query and return concatenated summaries of all pages found.
    """
    from langchain_community.tools import WikipediaQueryRun
    from langchain_community.utilities import WikipediaAPIWrapper
    
    wiki_search_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
    result = wiki_search_tool.run(query)

    # Extract and clean up summaries
    summaries = re.findall(r"Summary:\s*(.*?)(?=Page:|\Z)", result, re.DOTALL)
    concatenated_summary = "\n".join(s.strip().replace("\n", " ") for s in summaries)

    return concatenated_summary


