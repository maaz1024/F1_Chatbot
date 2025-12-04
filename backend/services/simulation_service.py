from services.fastf1_service import HARDCODED_WDC_2025

class WDCSimulationService:

    # FIA points table for 1–10
    POINTS_TABLE = {
        1: 25,
        2: 18,
        3: 15,
        4: 12,
        5: 10,
        6: 8,
        7: 6,
        8: 4,
        9: 2,
        10: 1
    }

    @staticmethod
    def simulate(results: dict | None = None):
        """
        Perform a WDC simulation.
        - If `results` is None → return current standings as-is.
        - If results are provided → apply points and return updated standings.
        """

        current = {row["Driver"]: row["Points"] for row in HARDCODED_WDC_2025}

        if results is None:
            return {
                "message": "Simulation executed with default (unsimulated) standings.",
                "standings": HARDCODED_WDC_2025
            }

        # Apply scoring
        for driver, position in results.items():
            if driver not in current:
                continue
            if position in WDCSimulationService.POINTS_TABLE:
                current[driver] += WDCSimulationService.POINTS_TABLE[position]

        # Convert back to sorted list
        updated_list = sorted(
            [
                {"Driver": d, "Points": pts}
                for d, pts in current.items()
            ],
            key=lambda x: x["Points"],
            reverse=True
        )

        # Assign new positions
        for i, row in enumerate(updated_list, start=1):
            row["Position"] = i

        return {
            "message": "Simulation complete.",
            "standings": updated_list
        }
