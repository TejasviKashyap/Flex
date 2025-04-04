import streamlit as st
import time
from typing import Annotated, List, Set, Optional, TypedDict
from pydantic import BaseModel
from operator import add
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import AnyMessage, add_messages, BaseMessage
from langgraph.managed import IsLastStep
from langgraph.managed.is_last_step import RemainingSteps
from langgraph.graph import StateGraph, END, START
import os

# Import necessary libraries for your LangGraph application
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain.schema import (
    HumanMessage,
    SystemMessage,
)

from app.core.state import MultiAgentState
from app.core.graph import build_financial_assistant_graph

# Setup the page configuration
st.set_page_config(
    page_title="FLEX - Financial Literacy Expert",
    page_icon="💰",
    layout="wide",
)

# CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #6B7280;
        text-align: center;
        margin-bottom: 2rem;
    }
    .user-message {
        background-color: #E5E7EB;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .assistant-message {
        background-color: #DBEAFE;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1E40AF;
    }
    .profile-section {
        background-color: #F3F4F6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "snapshot" not in st.session_state:
    st.session_state.snapshot = []

if "profile" not in st.session_state:
    st.session_state.profile = {
        "name": "N/A",
        "profession": "N/A",
        "income": "N/A",
        "expenses": "N/A"
    }

if "checkpointer" not in st.session_state:
    st.session_state.checkpointer = MemorySaver()

if "thread" not in st.session_state:
    st.session_state.thread = {"configurable": {"thread_id": "1"}, "recursion_limit": 15}

if "graph" not in st.session_state:
    # We'll initialize the graph in a function below
    st.session_state.graph = None

# Add placeholder for HF token
if "hf_token" not in st.session_state:
    st.session_state.hf_token = None

if "tavily_key" not in st.session_state:
    st.session_state.tavily_key = None

if "model_endpoint" not in st.session_state:
    st.session_state.model_endpoint = None

if "llm" not in st.session_state:
    st.session_state.llm = None

# State definition from your code


# Main app layout
st.markdown("<h1 class='main-header'>FLEX - Financial Literacy Expert</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Your personal guide to financial literacy and information</p>", unsafe_allow_html=True)

# Sidebar for API keys and settings
with st.sidebar:
    st.header("Configuration")
    
    # API key inputs
    hf_token = st.text_input("HuggingFace Token", type="password")
    tavily_key = st.text_input("Tavily API Key", type="password")
    model_endpoint = st.selectbox(
                    "Model", 
                    ["meta-llama/Meta-Llama-3.1-8B-Instruct", "meta-llama/Meta-Llama-3.1-70B-Instruct"],
                    index=0
                )
    
    # Save API keys to session state
    if st.button("Save API Keys"):
        st.session_state.hf_token = hf_token
        st.session_state.tavily_key = tavily_key
        st.session_state.model_endpoint = model_endpoint
        st.success("API keys saved!")

                # Initialize LLM
        ENDPOINT_URL = st.session_state.model_endpoint
        st.session_state.llm = HuggingFaceEndpoint(
            repo_id=ENDPOINT_URL,
            task="text-generation",
            max_new_tokens=1024,
            top_k=50,
            temperature=0.1,
            repetition_penalty=1.03,
            huggingfacehub_api_token=hf_token,
        )
        
        # Initialize the graph with the new API keys
        try:
            st.session_state.graph = build_financial_assistant_graph(
                hf_token = st.session_state.hf_token,
                tavily_key = st.session_state.tavily_key,
                checkpointer = st.session_state.checkpointer)
            
            st.success("Financial Assistant initialized successfully!")

        except Exception as e:
            st.error(f"Error initializing assistant: {str(e)}")

    # User Profile Section
    st.header("User Profile")
    with st.form("profile_form"):
        name = st.text_input("Name", value=st.session_state.profile["name"] if st.session_state.profile["name"] != "N/A" else "")
        profession = st.text_input("Profession", value=st.session_state.profile["profession"] if st.session_state.profile["profession"] != "N/A" else "")
        income = st.text_input("Income", value=st.session_state.profile["income"] if st.session_state.profile["income"] != "N/A" else "")
        expenses = st.text_input("Expenses", value=st.session_state.profile["expenses"] if st.session_state.profile["expenses"] != "N/A" else "")
        
        submitted = st.form_submit_button("Update Profile")
        if submitted:
            st.session_state.profile = {
                "name": name if name else "N/A",
                "profession": profession if profession else "N/A",
                "income": income if income else "N/A",
                "expenses": expenses if expenses else "N/A"
            }
            st.success("Profile updated!")

    # Show current profile info
    if st.session_state.profile["name"] != "N/A":
        st.markdown("### Current Profile")
        st.markdown(f"**Name:** {st.session_state.profile['name']}")
        st.markdown(f"**Profession:** {st.session_state.profile['profession']}")
        st.markdown(f"**Income:** {st.session_state.profile['income']}")
        st.markdown(f"**Expenses:** {st.session_state.profile['expenses']}")

# Chat interface
st.header("Chat with FLEX")

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"<div class='user-message'>{message['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='assistant-message'>{message['content']}</div>", unsafe_allow_html=True)


snapshot = None
if st.session_state.snapshot:
    snapshot = st.session_state.snapshot[0]


# Chat input
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Your question:", key="user_input")
    submit_button = st.form_submit_button("Send")

    if submit_button and user_input:
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Create a placeholder for the assistant's response
        with st.empty():
            st.markdown("<div class='assistant-message'>Thinking...</div>", unsafe_allow_html=True)
            
            try:
                if st.session_state.graph is None and st.session_state.hf_token:
                    st.session_state.graph = build_financial_assistant_graph(
                                                hf_token = st.session_state.hf_token,
                                                tavily_key = st.session_state.tavily_key,
                                                checkpointer = st.session_state.checkpointer)
                
                if st.session_state.graph is not None:
                    # Invoke the graph with the user input
                    result = st.session_state.graph.invoke({
                        'question': [user_input],
                    }, st.session_state.thread)
                    
                    # Get the answer from the result
                    answer = result['answer'][-1]
                else:
                    answer = "Please provide API keys in the sidebar to initialize the assistant."
            except Exception as e:
                answer = f"Error processing your request: {str(e)}"
        
        st.session_state.snapshot = list(st.session_state.graph.get_state(st.session_state.thread))
        

        # Add assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
        
        # Force a rerun to display the new messages
        st.rerun()

if st.session_state.snapshot:
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.expander("Question"):
            st.write(snapshot['question'][-1])
    with col2:
        with st.expander("Question with context"):
            st.write(snapshot['context_question'][-1])
    with col3:
        with st.expander("Answer"):
            st.write(snapshot['answer'][-1])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.expander("Domain"):
            if snapshot['domain']:
                st.write(snapshot['domain'])

    with col2:
        with st.expander("Question Type"):
            if snapshot['question_type']:
                st.write(snapshot['question_type'][-1])

    with col3:
        with st.expander("Named Entities Present"):
            if 'NER' in snapshot.keys() and snapshot['NER']:
                st.write(snapshot['NER'])

    with col4:
        with st.expander("Profile"):
            st.write("Name: " + snapshot['name'])
            st.write("Profession: " + snapshot['profession'])
            st.write("income: " + snapshot['income'])
            st.write("expenditure: " + snapshot['expenses'])


    with st.expander("Draft Answer"):
        st.write(snapshot['draft_answer'][-1])


# Add a disclaimer at the bottom
st.markdown("---")
st.caption("FLEX is a AI assistant for financial literacy education. It does not provide financial advice and should not be used for making investment decisions.")