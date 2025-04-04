import streamlit as st
from app.core.state import MultiAgentState
from langchain_huggingface import ChatHuggingFace
from langgraph.prebuilt import create_react_agent
from app.tools.rtd import get_stock_data, lookup_forex_rates
from app.prompts.rtd import rtd_prompt_template
from langchain.schema import HumanMessage


def rtd_node(state: MultiAgentState, llm = st.session_state.llm):
    model = ChatHuggingFace(llm=llm)
    rtd_agent = create_react_agent(model, [get_stock_data, lookup_forex_rates],
        prompt=rtd_prompt_template, state_schema=MultiAgentState)
    try:
        result = rtd_agent.invoke({
            "context_question": [('user', state['context_question'][-1])],
            "messages": state['messages']})
        
        return {'draft_answer': [result['messages'][-1].content]}
    except Exception as e:
        print(e)
        return {'draft_answer': ["I don't know"]}

