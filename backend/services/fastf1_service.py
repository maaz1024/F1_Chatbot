import fastf1
from datetime import datetime

HARDCODED_WDC_2025 = [
    {"Position": 1, "Driver": "Lando Norris", "Team": "McLaren", "Points": 408},
    {"Position": 2, "Driver": "Max Verstappen", "Team": "Red Bull Racing", "Points": 396},
    {"Position": 3, "Driver": "Oscar Piastri", "Team": "McLaren", "Points": 392},
    {"Position": 4, "Driver": "George Russell", "Team": "Mercedes", "Points": 309},
    {"Position": 5, "Driver": "Charles Leclerc", "Team": "Ferrari", "Points": 230},
    {"Position": 6, "Driver": "Lewis Hamilton", "Team": "Ferrari", "Points": 152},
    {"Position": 7, "Driver": "Andrea Kimi Antonelli", "Team": "Mercedes", "Points": 150},
    {"Position": 8, "Driver": "Alex Albon", "Team": "Williams", "Points": 73},
    {"Position": 9, "Driver": "Carlos Sainz", "Team": "Williams", "Points": 64},
    {"Position": 10, "Driver": "Isack Hadjar", "Team": "Racing Bulls", "Points": 51},
    {"Position": 11, "Driver": "Nico Hulkenberg", "Team": "Kick Sauber", "Points": 49},
    {"Position": 12, "Driver": "Fernando Alonso", "Team": "Aston Martin", "Points": 48},
    {"Position": 13, "Driver": "Oliver Bearman", "Team": "Haas", "Points": 41},
    {"Position": 14, "Driver": "Liam Lawson", "Team": "Racing Bulls", "Points": 38},
    {"Position": 15, "Driver": "Yuki Tsunoda", "Team": "Red Bull Racing", "Points": 33},
    {"Position": 16, "Driver": "Esteban Ocon", "Team": "Haas", "Points": 32},
    {"Position": 17, "Driver": "Lance Stroll", "Team": "Aston Martin", "Points": 32},
    {"Position": 18, "Driver": "Pierre Gasly", "Team": "Alpine", "Points": 22},
    {"Position": 19, "Driver": "Gabriel Bortoleto", "Team": "Kick Sauber", "Points": 19},
    {"Position": 20, "Driver": "Franco Colapinto", "Team": "Alpine", "Points": 0},
    {"Position": 21, "Driver": "Jack Doohan", "Team": "Alpine", "Points": 0},
]


class FastF1Service:

    @staticmethod
    def get_wdc_standings():
        """
        Returns the hardcoded 2025 live standings.
        Always works.
        """
        return HARDCODED_WDC_2025

    @staticmethod
    def get_next_race():
        """
        Uses FastF1 event schedule to return next race.
        This part of FastF1 is stable and works offline.
        """
        fastf1.Cache.enable_cache("cache")

        year = datetime.now().year
        schedule = fastf1.get_event_schedule(year)

        today = datetime.now().date()
        future = schedule[schedule["EventDate"].dt.date >= today]

        if future.empty:
            return {"message": "No upcoming races"}

        row = future.iloc[0]

        return {
            "round": int(row["RoundNumber"]),
            "raceName": row["EventName"],
            "date": row["EventDate"].strftime("%Y-%m-%d"),
            "location": row["Location"],
            "country": row["Country"],
        }
