import streamlit as st
from app.core.state import MultiAgentState
from langchain_huggingface import ChatHuggingFace
from app.prompts.editor import editor_agent_prompt
from langchain.schema import HumanMessage, SystemMessage


def editor_node(state: MultiAgentState, llm = st.session_state.llm):
    chat_history = state.get('chat_history', [])
    context_question = state.get('context_question', "")
    if context_question == "":
        context_question = state['question'][-1]
    
    model = ChatHuggingFace(llm=llm)
    messages = [SystemMessage(content=editor_agent_prompt.format(
        question=state['question'][-1],
        context_question=context_question,
        draft_answer=state['draft_answer'][-1],
        name=state['name'],
        profession=state['profession'],
        income=state['income'],
        expenses=state['expenses'],
        chat_history=chat_history)
    )]
    result = model.invoke(messages)
    
    return {'answer': [result.content], 'chat_history': [{'question': state['question'][-1], 'answer': result.content}]}