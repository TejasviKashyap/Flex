import streamlit as st
from app.core.state import MultiAgentState
from langchain_huggingface import ChatHuggingFace
from app.prompts.general import general_prompt
from langchain.schema import HumanMessage, SystemMessage

def general_assistant_node(state: MultiAgentState, llm = st.session_state.llm):
    messages = [SystemMessage(content=general_prompt.format(
        chat_history=state['chat_history'],
        context_question=state['context_question'][-1]
    )),
        HumanMessage(content=state['question'][-1])
    ]
    model = ChatHuggingFace(llm=llm)
    response = model.invoke(messages)
    
    return {"draft_answer": [response.content]}
