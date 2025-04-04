import streamlit as st
from app.core.state import MultiAgentState
from langchain_huggingface import ChatHuggingFace
from langgraph.prebuilt import create_react_agent
from app.tools.fintalk import wiki_search
from app.prompts.fintalk import financial_terms_prompt
from langchain.schema import HumanMessage

def financial_terms_node(state: MultiAgentState, llm = st.session_state.llm):
    model = ChatHuggingFace(llm=llm)
    financial_terms_agent = create_react_agent(model, [wiki_search],
        prompt=financial_terms_prompt, state_schema=MultiAgentState)

    try:
        result = financial_terms_agent.invoke({
            "context_question": [('user', state['context_question'][-1])],
            "remaining_steps": [('ai', str(state['remaining_steps']))],
            "messages": state['messages']})
        
        return {'draft_answer': [result['messages'][-1].content]}
    except Exception as e:
        print(e)
        return {'draft_answer': ["I don't know"]}
