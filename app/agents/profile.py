
import streamlit as st
from app.core.state import MultiAgentState
from langchain_huggingface import ChatHuggingFace
from app.prompts.profile import profile_prompt
from langchain.schema import HumanMessage, SystemMessage

# Node definitions
def profile_node(state: MultiAgentState, llm = st.session_state.llm):
    messages = [
        SystemMessage(content=profile_prompt),
        HumanMessage(content=state['question'][-1])
    ]
    model = ChatHuggingFace(llm=llm)
    response = model.invoke(messages)
    try:
        vals = response.content.split(',')
        name = state.get('name', 'N/A')
        profession = state.get('profession', 'N/A')
        income = state.get('income', 'N/A')
        expenses = state.get('expenses', 'N/A')
        if "N/A" not in vals[0] and vals[0].strip != '':
            name = vals[0]
        if "N/A" not in vals[1] and vals[1].strip != '':
            profession = vals[1]
        if "N/A" not in vals[2] and vals[2].strip != '':
            income = vals[2]
        if "N/A" not in vals[3] and vals[3].strip != '':
            expenses = vals[3]
        return {
            'name': name,
            'profession': profession,
            'income': income,
            'expenses': expenses,
        }
    except Exception as e:
        print(e)
        name = state.get('name', 'N/A')
        profession = state.get('profession', 'N/A')
        income = state.get('income', 'N/A')
        expenses = state.get('expenses', 'N/A')
        return {
            'name': name,
            'profession': profession,
            'income': income,
            'expenses': expenses,
        }