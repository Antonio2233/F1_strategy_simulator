
import math
import numpy as np
from simulator import *

# -------------------------- Utils ---------------------------------
def pretty_time(seconds: float) -> str:
    m, s = divmod(seconds, 60)
    return f"{int(m):02d}:{s:06.3f}"


def compare_strategies(sim: RaceSimulator, strategies: List[Strategy], seed: Optional[int] = 42):
    rng = np.random.default_rng(seed)
    events = sim.sample_events() # fix the same events for all strategies
    results = []
    for st in strategies:
        # Use same noise seed for fairness
        sim.rng = np.random.default_rng(seed)
        res = sim.simulate(st, events=events)
        results.append(res)
    results.sort(key=lambda r: r['total_time'])
    return results



from itertools import product

def generate_strategies(total_laps, compounds, max_stops):
    strategies = []

    # Generate strategies for 1-stop (2 stints), 2-stop (3 stints), etc. 
    # N stints = N stops + 1
    for stops in range(1, max_stops + 1):
        stints_count = stops + 1  # N stints = stops + 1


        # Generate all combinations of compounds for the stints
        for combo in product(compounds, repeat=stints_count):
            
            # Generate all possible lap splits that add up to total_laps
            def generate_lap_splits(n, k, min_laps=1):
                if k == 1:
                    if n >= min_laps:
                        yield [n]
                    return
                for i in range(min_laps, n - min_laps*(k-1) + 1):
                    for rest in generate_lap_splits(n - i, k - 1, min_laps):
                        yield [i] + rest

            # Skip strategies using only one compound
            if len({c.name for c in combo}) < 2:
                continue  

            for laps_split in generate_lap_splits(total_laps, stints_count, min_laps=1):
                stints = [Stint(comp, laps) for comp, laps in zip(combo, laps_split)]
                name = f"{stints_count-1}-stop " + "→".join([s.compound.name for s in stints])
                strategies.append(Strategy(name, stints))

    return strategies
