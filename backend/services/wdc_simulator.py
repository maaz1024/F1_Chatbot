POINTS = {
    1: 25, 2: 18, 3: 15, 4: 12, 5: 10,
    6: 8, 7: 6, 8: 4, 9: 2, 10: 1
}

from services.fastf1_service import FastF1Service

def run_simulation(finishing_positions=None):
    standings = FastF1Service.get_wdc_standings()
    points_map = {d["Driver"]: d["Points"] for d in standings}

    if finishing_positions:
        for driver, pos in finishing_positions.items():
            if pos in POINTS:
                points_map[driver] += POINTS[pos]
    else:
        return {"error": "No finishing positions provided."}

    sorted_table = sorted(points_map.items(), key=lambda x: x[1], reverse=True)
    return [{"Driver": d, "Points": p} for d, p in sorted_table]
