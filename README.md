# 🏎️ F1 Assistant & Championship Simulator

### Live App: [F1 Assistant Streamlit App](https://maaz1024-f1chatbot.streamlit.app/)

A full-stack AI-powered Formula 1 application that combines a RAG-based chatbot with real-time race data analysis and championship simulations.

## 🌟 Features

### 1. 🤖 F1 QnA Chatbot (RAG Agent)
- Intelligent Agent: Uses LangGraph to orchestrate a research agent that can browse the web and access internal knowledge bases.
- LLM Power: Powered by Groq (Llama 3) for ultra-fast inference.
- Context Aware: Capable of answering questions about current standings, technical regulations, and driver history.

### 2. 📊 Live Standings
- Fetches real-time World Driver Championship (WDC) points directly from the Ergast/OpenF1 APIs.
- Displays formatted standings with team associations.

### 3. 🧮 WDC Championship Simulator
- Scenario Modeling: Allows users to input hypothetical race results for the upcoming Abu Dhabi Grand Prix.
- Points Calculation: Automatically calculates the new championship order based on the user's input.
- Podium Visualization: Renders a dynamic, CSS-styled podium for the top 3 projected finishers.

## 🏗️ Architecture
The project follows a decoupled Client-Server architecture:
- Frontend: Built with Streamlit. Handles user UI, visualizations, and simulation inputs.
- Backend: Built with FastAPI. Manages the LangChain agents, data processing, and external API calls.

Tech Stack (The internal structure of the LangGraph agent used for the chatbot)
- Frontend: Python, Streamlit, Pandas, CSS
- Backend: Python, FastAPI, Uvicorn
- AI / LLM: LangGraph, Groq API (Llama 3)
- Data Sources: FastF1
- Deployment: Streamlit Community Cloud (Frontend), Render (Backend)