import streamlit as st
from app.core.state import MultiAgentState
from langchain_huggingface import ChatHuggingFace
from app.prompts.domain import domain_classification_prompt
from langchain.schema import HumanMessage, SystemMessage

def domain_node(state: MultiAgentState, llm = st.session_state.llm):
    messages = [
        SystemMessage(content=domain_classification_prompt),
        HumanMessage(content=state['question'][-1])
    ]
    model = ChatHuggingFace(llm=llm)
    response = model.invoke(messages)

    if 'general' in response.content.lower():
        return {
            'domain': 'general',
            'context_question': [state['question'][-1]],
            'question_type': ['GENERAL']
        }
    elif 'finance' in response.content.lower():
        return {
            'domain': 'finance',
        }
    else:
        return {
            'domain': 'general',  # Default to 'general' if neither is found
            'context_question': [state['question'][-1]],
            'question_type': ['GENERAL']
        }
