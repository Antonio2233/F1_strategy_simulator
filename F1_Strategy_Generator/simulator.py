
from typing import List, Tuple, Optional, Dict
from models import *

# ----------------------- Race Simulator  --------------------------
class RaceSimulator:
    def __init__(self, track: Track, car: Car, rng: Optional[np.random.Generator] = None):
        self.track = track
        self.car = car
        self.rng = rng or np.random.default_rng(42)

    def sample_events(self, p_sc: float = 0.12, p_vsc: float = 0.20) -> List[Event]:
        events: List[Event] = []
        # Safety Car probability
        if self.rng.random() < p_sc:
            start = int(self.rng.integers(5, self.track.laps - 5))
            dur = int(self.rng.integers(2, 6))
            events.append(Event('SC', start, dur, pit_loss_factor=0.55, lap_time_factor=1.15))
        # Virtual Safety Car (VSC) Probability
        if self.rng.random() < p_vsc:
            start = int(self.rng.integers(5, self.track.laps - 5))
            dur = int(self.rng.integers(1, 4))
            events.append(Event('VSC', start, dur, pit_loss_factor=0.70, lap_time_factor=1.07))
        return events

    def simulate(self, strategy: Strategy, events: Optional[List[Event]] = None, noise: float = 0.10) -> Dict:
        """
        Simulates a race for a given strategy.
        - events: list of events (if None, they are sampled)
        - noise: random variability (standard deviation in seconds) for lap-to-lap performance
        Returns a dict with lap times, pit stops, events, and total time.
        """
        if sum(s.laps for s in strategy.stints) != self.track.laps:
            raise ValueError("The sum of stint laps must equal the total number of track laps.")

        events = events if events is not None else self.sample_events()
        event_by_lap = self._expand_events(events)

        lap_times: List[float] = []
        pit_laps: List[int] = []

        # Fuel model: assume uniform consumption and linear penalty
        fuel_per_lap = self.car.start_fuel_kg / self.track.laps
        fuel_kg = self.car.start_fuel_kg

        cur_lap = 1
        for stint_idx, stint in enumerate(strategy.stints):
            comp = stint.compound
            for stint_lap in range(1, stint.laps + 1):
                # Base pace
                lt = self.track.base_lap_time
                # Compound effect
                lt += comp.perf_delta
                # Warmup effect
                if stint_lap <= comp.warmup_laps:
                    lt -= self.track.tyre_warmup * (comp.warmup_laps - stint_lap + 1) / comp.warmup_laps
                # Linear degradation
                lt += comp.deg_per_lap * (stint_lap - 1)
                # Cliff effect if applicable
                if comp.cliff_lap is not None and stint_lap > comp.cliff_lap:
                    lt += comp.cliff_penalty * (stint_lap - comp.cliff_lap)
                # Fuel effect (per 10 kg)
                lt += self.track.fuel_effect * (fuel_kg / 10.0)
                # Random variability
                lt += self.rng.normal(0.0, noise)
                # Event effect (SC/VSC)
                if cur_lap in event_by_lap:
                    e = event_by_lap[cur_lap]
                    lt *= e.lap_time_factor
                lap_times.append(lt)

                # Update fuel
                fuel_kg -= fuel_per_lap
                cur_lap += 1

            # Pit stop if not the last stint
            if stint_idx < len(strategy.stints) - 1:
                pit_time = self.track.pit_loss
                # Adjust pit loss if the stop occurs during an event
                if (cur_lap - 1) in event_by_lap:
                    pit_time *= event_by_lap[cur_lap - 1].pit_loss_factor
                lap_times[-1] += pit_time  # add the loss at the end of the lap before the stop
                pit_laps.append(cur_lap - 1)

        total_time = sum(lap_times)
        return {
            'strategy': strategy,
            'lap_times': lap_times,
            'pit_laps': pit_laps,
            'events': events,
            'total_time': total_time,
        }

    def _expand_events(self, events: List[Event]) -> Dict[int, Event]:
        by_lap: Dict[int, Event] = {}
        for e in events:
            for l in range(e.start_lap, min(self.track.laps, e.start_lap + e.duration_laps)):
                by_lap[l] = e
        return by_lap
