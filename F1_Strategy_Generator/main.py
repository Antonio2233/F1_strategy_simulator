import json
import pandas as pd

from models import *
from simulator import *
from utils import pretty_time,generate_strategies,compare_strategies

if __name__ == "__main__":
    # Track definition (example: Barcelona, 66 laps)
    track = Track(
        name="Barcelona",
        laps=66,
        base_lap_time=76.5,   # 1:16.500 as hypothetical base
        pit_loss=19.5,        # average pit stop loss
        fuel_effect=0.28,     # s per 10 kg
        tyre_warmup=0.30,
    )

    # Tyre compound definitions (approximate parameters)
    S = Compound("S", perf_delta=-0.6, deg_per_lap=0.035, cliff_lap=18, cliff_penalty=0.10, warmup_laps=1)
    M = Compound("M", perf_delta=0.0, deg_per_lap=0.028, cliff_lap=26, cliff_penalty=0.08, warmup_laps=1)
    H = Compound("H", perf_delta=+0.4, deg_per_lap=0.022, cliff_lap=40, cliff_penalty=0.06, warmup_laps=1)

    compounds = [S, M, H]

    # max - 110.0 kg
    # min - 100.0 kg
    car = Car(start_fuel_kg=105.0)

    sim = RaceSimulator(track, car)

    MAX_PIT_STOP = 2

    all_strats = generate_strategies(total_laps=track.laps, compounds=compounds, max_stops=MAX_PIT_STOP)
    print(f" {len(all_strats)} strategies generated")
    # print(all_strats)  


    results = compare_strategies(sim, all_strats, seed=123)

    file = []

    print(f"\nTrack: {track.name} | Laps: {track.laps}\n")
    for r in results:
        st = r['strategy']
        # print(f"{st.name:15s}  Total: {pretty_time(r['total_time'])}  Pits on Laps: {r['pit_laps']}")
        file.append({
            "Strategy": f"{st.name:15s}",   
            "Total": pretty_time(r["total_time"]),
            "Pit in Laps": r["pit_laps"]
        })


    df = pd.DataFrame(file)

    df.to_csv("simulations.csv",index=False)
    try:
        import matplotlib.pyplot as plt
        best = results[0]
        lt = best['lap_times']
        plt.figure()
        plt.plot(range(1, len(lt)+1), lt)
        plt.xlabel('Lap')
        plt.ylabel('LapTime (s)')
        plt.title(f"Best Strategy: {best['strategy'].name}")
        plt.tight_layout()
        plt.show()
    except Exception:
        pass
