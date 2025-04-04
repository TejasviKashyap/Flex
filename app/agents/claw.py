import streamlit as st
from app.core.state import MultiAgentState
from langchain_huggingface import ChatHuggingFace
from langgraph.prebuilt import create_react_agent
from app.tools.claw import tavily_search
from app.prompts.claw import canadian_rules_prompt
from langchain.schema import HumanMessage

def canadian_rules_node(state: MultiAgentState, llm = st.session_state.llm):
    model = ChatHuggingFace(llm=llm)
    canadian_rules_agent = create_react_agent(model, [tavily_search],
        prompt=canadian_rules_prompt, state_schema=MultiAgentState)
    try:
        result = canadian_rules_agent.invoke({
            "context_question": [('user', state['context_question'][-1])],
            "messages": state['messages']})
        
        return {'draft_answer': [result['messages'][-1].content]}
    except Exception as e:
        print(e)
        return {'draft_answer': ["I don't know"]}
