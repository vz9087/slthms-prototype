# Simulation engine: in-memory ladle simulator
import numpy as np
from collections import deque
from datetime import datetime
import pandas as pd

LADLE_IDS = ["L-01", "L-02", "L-03", "L-04", "L-05", "L-06"]
PLANT_ZONES = ["TLC Pit", "Converter Bay", "LF-1", "LF-2", "RH", "Twin LF", "Caster"]

def init_state(buffer_size=30):
    now = datetime.utcnow()
    sim = {}
    for lid in LADLE_IDS:
        base_temp = 1500 + np.random.randint(-30, 30)
        sim[lid] = {
            "ladle_id": lid,
            "temperature": int(base_temp),
            "stress": int(np.random.uniform(50, 70)),
            "vibration": round(np.random.uniform(0.3, 0.5), 2),
            "location": np.random.choice(PLANT_ZONES),
            "times": deque(maxlen=buffer_size),
            "temps": deque(maxlen=buffer_size),
        }
        for i in range(10):
            t = now - pd.Timedelta(seconds=(10 - i) * 3)
            sim[lid]["times"].append(t)
            sim[lid]["temps"].append(sim[lid]["temperature"] + np.random.randn())
    return sim

def step(sim, buffer_size=30, force_anomaly=None):
    now = datetime.utcnow()
    for lid, ladle in sim.items():
        ladle["temperature"] = int(np.clip(ladle["temperature"] + np.random.randint(-8, 9), 1400, 1700))
        ladle["stress"] = int(np.clip(ladle["stress"] + np.random.randint(-3, 4), 30, 95))
        ladle["vibration"] = round(np.clip(ladle["vibration"] + np.random.uniform(-0.05, 0.05), 0.1, 1.0), 2)
        if np.random.rand() < 0.15:
            ladle["location"] = np.random.choice(PLANT_ZONES)
        ladle["times"].append(now)
        ladle["temps"].append(ladle["temperature"])
    if force_anomaly:
        lid = force_anomaly.get("ladle_id")
        if lid in sim:
            for k, v in force_anomaly.items():
                if k != "ladle_id":
                    sim[lid][k] = v
            sim[lid]["times"].append(now)
            sim[lid]["temps"].append(sim[lid]["temperature"])
    return sim
