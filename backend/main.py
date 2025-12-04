from fastapi import FastAPI
from pydantic import BaseModel
from agent.graph import agent_runner
from agent.tools import fastf1_tool, wdc_simulation_tool
from services.fastf1_service import FastF1Service
from services.wdc_simulator import run_simulation

app = FastAPI(title="F1 AI Assistant")

class ChatRequest(BaseModel):
    message: str

class SimulationRequest(BaseModel):
    finishing_positions: dict | None = None

@app.post("/chat")
async def chat(req: ChatRequest):
    output_state = await agent_runner.ainvoke({"message": req.message})
    return {"response": output_state["final_output"]}

@app.get("/standings")
def standings():
    return FastF1Service.get_wdc_standings()

@app.get("/next_race")
def upcoming():
    return FastF1Service.get_next_race()

@app.post("/simulate")
def simulate(req: SimulationRequest):
    result = run_simulation(req.finishing_positions)
    return {"standings": result}
