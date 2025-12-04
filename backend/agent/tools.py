from services.fastf1_service import FastF1Service
from services.simulation_service import WDCSimulationService

async def fastf1_tool(intent: str):
    """
    intent is one of:
    - 'standings'
    - 'next_race'

    Tools NEVER interpret user text.
    Tools NEVER apply heuristics.
    Tools simply run and return raw data.
    """

    if intent == "standings":
        return FastF1Service.get_wdc_standings()

    if intent == "next_race":
        return FastF1Service.get_next_race()

    return "Unknown FastF1 tool intent."


async def wdc_simulation_tool(_):
    """
    Simulation tool.
    The graph determines when to call this tool.
    """
    return WDCSimulationService.simulate()
