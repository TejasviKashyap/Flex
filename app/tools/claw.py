import streamlit as st
from langchain_core.tools import tool

@tool(return_direct=True)
def tavily_search(query: str) -> str:
    """
    Search using tavily for a given query and return a string
    with the answer and summary from the search results.
    """
    from langchain_tavily import TavilySearch, TavilyExtract
    
    ans = ""
    search_tool = TavilySearch(max_results=3, tavily_api_key=st.session_state.tavily_key, search_depth="basic",
                              include_answer=True)
    result = search_tool.run(query)
    ans += result['answer']

    urls = []
    for i in result['results']:
        urls.append(i['url'])
    extract_tool = TavilyExtract(tavily_api_key=st.session_state.tavily_key, extract_depth="basic")
    result = extract_tool.run({'urls': urls})
    for i in result['results']:
        try:
            ans += i['raw_content']
        except Exception as e:
            print(e)

    return ans
