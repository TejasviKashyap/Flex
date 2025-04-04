import streamlit as st
from app.core.state import MultiAgentState
from langchain_huggingface import ChatHuggingFace
from app.prompts.context import context_prompt
from langchain.schema import HumanMessage, SystemMessage


def context_node(state: MultiAgentState, llm = st.session_state.llm):
    chat_history = state.get('chat_history', [])
    messages = [
        SystemMessage(content=context_prompt.format(
            chat_history=chat_history,
            name=state['name'],
            profession=state['profession'],
            income=state['income'],
            expenses=state['expenses'])
        ),
        HumanMessage(content=state['question'][-1])
    ]
    model = ChatHuggingFace(llm=llm)
    response = model.invoke(messages)

    if 'N/A' not in response.content:
        ner = True
        return {'NER': ner, 'context_question': [response.content]}
    else:
        ner = False
        return {'NER': ner, 'context_question': [state['question'][-1]], 'draft_answer': ["Question has missing context"]}