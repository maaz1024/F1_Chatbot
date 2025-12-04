🏎️ F1 Assistant & Championship Simulator

Live App: https://maaz1024-f1chatbot.streamlit.app/

A full-stack AI-powered Formula 1 application that combines a RAG-based chatbot with real-time race data analysis and championship simulations.

🌟 Features

1. 🤖 F1 QnA Chatbot (RAG Agent)

Intelligent Agent: Uses LangGraph to orchestrate a research agent that can browse the web and access internal knowledge bases.

LLM Power: Powered by Groq (Llama 3) for ultra-fast inference.

Context Aware: Capable of answering questions about current standings, technical regulations, and driver history.

2. 📊 Live Standings

Fetches real-time World Driver Championship (WDC) points directly from the Ergast/OpenF1 APIs.

Displays formatted standings with team associations.

3. 🧮 Championship Simulator

Scenario Modeling: Allows users to input hypothetical race results for upcoming Abu Dhabi Grand Prix.

Points Calculation: Automatically calculates the new championship order based on the user's input.

Podium Visualization: Renders a dynamic, CSS-styled podium for the top 3 projected finishers.

🏗️ Architecture

The project follows a decoupled Client-Server architecture:

Frontend: Built with Streamlit. Handles user UI, visualizations, and simulation inputs.

Backend: Built with FastAPI. Manages the LangChain agents, data processing, and external API calls.

(The internal structure of the LangGraph agent used for the chatbot)

Tech Stack

Component

Technologies

Frontend

Python, Streamlit, Pandas, CSS

Backend

Python, FastAPI, Uvicorn

AI / LLM

LangChain, LangGraph, Groq API (Llama 3)

Data Sources

DuckDuckGo Search, Wikipedia API, FastF1

Deployment

Streamlit Community Cloud (Frontend), Render (Backend)

🚀 Local Installation

Prerequisites

Python 3.10+

Groq API Key

1. Clone the Repository

git clone [https://github.com/maaz1024/F1_Chatbot.git](https://github.com/maaz1024/F1_Chatbot.git)
cd F1_Chatbot


2. Backend Setup

Navigate to the backend and install dependencies:

# Create virtual env (optional but recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt


Create a .env file in backend/ with your credentials:

GROQ_API_KEY=gsk_...

Run the Backend server:

# Run from the root directory
uvicorn backend.main:app --reload


Backend will run at http://localhost:8000

3. Frontend Setup

Open a new terminal, activate the environment, and run Streamlit:

streamlit run frontend/app.py


Frontend will launch in your browser.

☁️ Deployment Guide

Backend (Render)

The backend is deployed as a Web Service on Render.

Build Command: pip install -r requirements.txt

Start Command: uvicorn backend.main:app --host 0.0.0.0 --port $PORT

Environment Variables: GROQ_API_KEY, PYTHONPATH=.

Frontend (Streamlit Cloud)

The frontend is hosted on Streamlit Community Cloud.

Connected directly to the GitHub repository.

Main File: frontend/app.py

API Connection: The API_URL in app.py points to the live Render backend.

📂 Project Structure

F1_Chatbot/
├── backend/
│   ├── agent/             # LangGraph agent logic (nodes, edges)
│   ├── services/          # Business logic (simulation, data fetchers)
│   ├── main.py            # FastAPI entry point
│   └── .env               # API Keys (Local only)
├── frontend/
│   ├── app.py             # Main Streamlit application
│   └── style.css          # Custom styling
├── requirements.txt       # Project dependencies
└── README.md              # Documentation


🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

