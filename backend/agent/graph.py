from dataclasses import dataclass
from langgraph.graph import StateGraph, END
from agent.llm import llm
from agent.memory import Memory
from agent.tools import fastf1_tool, wdc_simulation_tool
from datetime import datetime
import re


# STATE MODEL
@dataclass
class State:
    message: str
    tool: str | None = None
    tool_output: str | None = None
    final_output: str | None = None


SYSTEM_PROMPT = """
You are an expert Formula 1 assistant.

Rules:
- Only answer in the context of Formula 1.
- If a term has multiple meanings, ALWAYS choose the F1 meaning.
- Never mention tools, backend, JSON, FastF1, or implementation details.
- Be concise, accurate, and domain-correct.
"""



# ROUTER NODE — DECIDE WHICH TOOL TO CALL
async def llm_node(state: State):

    text = state.message.lower()

    if ("wdc" in text or "leader" in text or "championship" in text) and "2025" in text:
        state.tool = "wdc"
        return state.__dict__

    # HISTORICAL QUESTIONS (older than last season)
    years = re.findall(r"\b(19|20)\d{2}\b", text)
    if years:
        year = int(years[0])
        current_year = datetime.now().year
        if year < current_year - 1:
            state.tool = "general_f1"
            return state.__dict__


    routing_prompt = f"""
    {SYSTEM_PROMPT}

    Classify the user message into EXACTLY one label:

    "wdc"         → current standings, points, championship leader
    "leader"      → specifically asking who is leading NOW
    "next_race"   → upcoming GP
    "simulate"    → simulation request
    "general_f1"  → history, rules, definitions, strategy, non-live info

    User message: "{state.message}"

    Respond ONLY with one label.
    """

    decision = llm.invoke(routing_prompt).content.strip().lower()

    if decision not in ["wdc", "leader", "next_race", "simulate", "general_f1"]:
        decision = "general_f1"

    state.tool = decision
    return state.__dict__



# TOOL EXECUTION NODE — FASTF1, SIMULATION, OR NONE
async def tool_node(state: State):

    if state.tool in ["wdc", "leader"]:
        state.tool_output = await fastf1_tool("standings")

    elif state.tool == "next_race":
        state.tool_output = await fastf1_tool("next_race")

    elif state.tool == "simulate":
        state.tool_output = await wdc_simulation_tool(None)

    else:
        state.tool_output = None

    return state.__dict__


# POSTPROCESSING
async def postprocess_node(state: State):

    if state.tool == "general_f1":
        response = llm.invoke(
            f"""{SYSTEM_PROMPT}

        User question: "{state.message}"
        Answer clearly and concisely:
        """
        ).content

        state.final_output = response
        Memory.append(f"Assistant: {response}")
        return state.__dict__

    # Raw tool output → rewrite cleanly
    post_prompt = f"""
    {SYSTEM_PROMPT}

    Here is structured F1 data:

    {state.tool_output}

    Rewrite this into a natural, correct explanation.
    Do NOT mention tools or structure.
    User asked: "{state.message}"
    """

    final = llm.invoke(post_prompt).content
    state.final_output = final
    Memory.append(f"Assistant: {final}")
    return state.__dict__


# GRAPH
graph = StateGraph(State)

graph.add_node("llm_node", llm_node)
graph.add_node("tool_node", tool_node)
graph.add_node("postprocess_node", postprocess_node)

graph.set_entry_point("llm_node")

graph.add_edge("llm_node", "tool_node")
graph.add_edge("tool_node", "postprocess_node")
graph.add_edge("postprocess_node", END)

agent_runner = graph.compile()
