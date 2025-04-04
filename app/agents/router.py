import streamlit as st
from app.core.state import MultiAgentState
from langchain_huggingface import ChatHuggingFace
from app.prompts.router import question_category_prompt
from langchain.schema import HumanMessage, SystemMessage

def router_node(state: MultiAgentState, llm = st.session_state.llm):
    messages = [
        SystemMessage(content=question_category_prompt),
        HumanMessage(content=state['context_question'][-1])
    ]
    model = ChatHuggingFace(llm=llm)
    response = model.invoke(messages)
    response = response.content.strip()
    
    if response not in ['CANADIAN_RULES', 'FINANCE_TERMS', 'RTD', 'GENERAL']:
        response = 'GENERAL'
    
    return {'question_type': [response]}

