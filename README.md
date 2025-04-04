# FLEX: Financial Literacy Expert Assistant

FLEX is an open-source AI-powered assistant designed to help users understand financial concepts, laws, and real-time market data using LangGraph and local LLMs like LLaMA 3.1.

## 🔧 Features

- Tool-calling agent with LangGraph
- Multi-step tool planning using LLaMA 3.1
- Real-time data via Yahoo Finance and AlphaVantage
- Search + Extraction via Tavily API
- Wikipedia support for educational queries

## 🧠 Tech Stack

- 🦙 LLaMA 3.1 8B/LLaMA 3.1 70B (HF Transformers)
- 🔄 LangGraph (tool-agent workflows)
- 🌐 Streamlit frontend
- 🧰 Tools: Tavily, Wikipedia, Yahoo Finance, Alphavantage

## 🚀 Getting Started

1. Clone the repo
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run the app:
```bash
streamlit run main.py
```